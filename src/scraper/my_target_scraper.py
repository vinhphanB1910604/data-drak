import random
import time
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from src.utils.database_handler import DatabaseHandler
import pandas as pd

class MyTargetScraper:
    def __init__(self, max_workers=1):
        self.base_url = "https://masothue.com/tra-cuu-ma-so-thue-theo-tinh/can-tho-96"
        self.db_handler = DatabaseHandler(db_path="data-grak.db")
        self.user_agent = UserAgent()
        self.session = requests.Session()

    def get_random_user_agent(self):
        return self.user_agent.random

    def send_request(self, url):
        headers = {"User-Agent": self.get_random_user_agent()}
        try:
            r = self.session.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            print(f"[REQUEST ERROR] {e}")
            return None

    def parse_company_data(self, page_source):
        soup = BeautifulSoup(page_source, "html.parser")
        company_data = []

        rows = soup.select("table.table-hover.table-bordered tbody tr")
        for row in rows:
            cols = row.find_all("td")
            company = {
                "name": cols[1].get_text(strip=True),
                "tax_id": cols[2].get_text(strip=True),
                "abbreviation": "",
                "address": cols[3].get_text(strip=True),
                "phone": cols[4].get_text(strip=True),
                "representative": cols[5].get_text(strip=True),
                "status": cols[6].get_text(strip=True),
                "detail_url": cols[1].find("a")['href'] if cols[1].find("a") else ""
            }
            company_data.append(company)

        return company_data

    def parse_detail_page(self, url):
        full_url = f"https://masothue.com{url}"
        html = self.send_request(full_url)
        if not html:
            return {}

        soup = BeautifulSoup(html, "html.parser")
        detail_data = {}

        def extract(label):
            tag = soup.find("td", string=label)
            if tag and tag.find_next_sibling("td"):
                return tag.find_next_sibling("td").get_text(strip=True)
            return ""

        detail_data["activity_date"] = extract("Ngày hoạt động")
        detail_data["tax_office"] = extract("Quản lý bởi")
        detail_data["company_type"] = extract("Loại hình DN")
        detail_data["main_business"] = extract("Ngành nghề chính")
        detail_data["last_updated"] = soup.find("span", class_="timeago")\
            .get("title", "") if soup.find("span", class_="timeago") else ""

        return detail_data

    def save_to_db(self, companies):
        for c in companies:
            self.db_handler.insert_company(c)

    def export_to_excel(self, all_companies):
        # Tách dữ liệu đầy đủ và thiếu thông tin
        full_info_companies = [c for c in all_companies if all(v != "" for v in c.values())]
        missing_info_companies = [c for c in all_companies if any(v == "" for v in c.values())]

        # Xuất ra 2 sheet trong Excel
        with pd.ExcelWriter("companies_data.xlsx") as writer:
            pd.DataFrame(full_info_companies).to_excel(writer, sheet_name="Full Info", index=False)
            pd.DataFrame(missing_info_companies).to_excel(writer, sheet_name="Missing Info", index=False)

        print("Dữ liệu đã được xuất ra file Excel.")

    def start(self):
        all_companies = []
        seen_tax_ids = set()
        page = 1

        while True:
            url = f"{self.base_url}?page={page}" if page > 1 else self.base_url
            print(f"⏳ Đang cào page {page} …")
            html = self.send_request(url)
            if not html:
                print("Không thể truy cập hoặc hết page.")
                break

            batch = self.parse_company_data(html)
            if not batch:
                print("– Không tìm thấy DN trên page này, dừng.")
                break

            new_batch = [c for c in batch if c["tax_id"] not in seen_tax_ids]
            if not new_batch:
                print("– Toàn bộ DN đã cào trước đó, dừng pagination.")
                break

            for c in new_batch:
                print(c)  # In dữ liệu của mỗi công ty để kiểm tra
                if c["detail_url"]:
                    detail = self.parse_detail_page(c["detail_url"])
                    c.update(detail)
                time.sleep(random.uniform(1, 2))

            all_companies.extend(new_batch)
            seen_tax_ids.update(c["tax_id"] for c in new_batch)

            page += 1
            time.sleep(random.uniform(2, 4))

        if all_companies:
            print(f"\n🎉 Tổng cộng cào được {len(all_companies)} DN mới. Đang lưu vào DB…")
            self.save_to_db(all_companies)
            self.export_to_excel(all_companies)
            print(f"✅ Đã lưu {len(all_companies)} DN vào database.")
        else:
            print("⚠️ Không tìm thấy DN nào mới.")

        self.db_handler.close()

# Chạy scraper
scraper = MyTargetScraper()
scraper.start()
