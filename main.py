import os
from src.scraper.my_target_scraper import MyTargetScraper

# 🔁 Xoá file database và output nếu tồn tại
if os.path.exists("data-drak.db"):
    os.remove("data-drak.db")
    print("🗑️ Đã xoá file database cũ: data-drak.db")

if os.path.exists("output.xlsx"):
    os.remove("output.xlsx")
    print("🗑️ Đã xoá file output cũ: output.xlsx")

if __name__ == "__main__":
    scraper = MyTargetScraper()
    scraper.start()
