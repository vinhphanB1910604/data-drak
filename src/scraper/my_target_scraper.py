import random
import time
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from src.utils.database_handler import DatabaseHandler

class MyTargetScraper:
    def __init__(self, max_workers=1):
        self.base_url = "https://masothue.com/tra-cuu-ma-so-thue-theo-tinh/phuong-xuan-khanh-579"
        self.db_handler = DatabaseHandler(db_path="data-grak.db")
        self.user_agent = UserAgent()

    def get_random_user_agent(self):
        return self.user_agent.random

    def send_request(self, url):
        headers = {"User-Agent": self.get_random_user_agent()}
        try:
            r = requests.get(url, headers=headers, timeout=10)
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
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) < 7:
                continue

            company = {
                "name": cols[1].strip(),
                "tax_id": cols[2].strip(),
                "abbreviation": "",  # Không có thì để trống
                "address": cols[3].strip(),
                "phone": cols[4].strip(),
                "representative": cols[5].strip(),
                "status": cols[6].strip()
            }

            # Loại bỏ ký tự không hợp lệ (nếu có)
            for key in company:
                company[key] = ''.join(c for c in company[key] if c.isprintable())

            company_data.append(company)

        return company_data


    def save_to_db(self, companies):
        for c in companies:
            self.db_handler.insert_company(c)

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

            print(f"→ Page {page}: tìm được {len(batch)} DN, trong đó {len(new_batch)} DN mới.")
            all_companies.extend(new_batch)
            seen_tax_ids.update(c["tax_id"] for c in new_batch)

            page += 1
            time.sleep(random.uniform(1, 2))

        if all_companies:
            print(f"\n🎉 Tổng cộng cào được {len(all_companies)} DN mới. Đang lưu vào DB…")
            self.save_to_db(all_companies)
            print(f"✅ Đã lưu {len(all_companies)} DN vào database.")
        else:
            print("⚠️ Không tìm thấy DN nào mới.")
            
        self.db_handler.close()
