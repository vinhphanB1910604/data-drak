import sqlite3

class DatabaseHandler:
    def __init__(self, db_path="data-drak.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tax_id TEXT UNIQUE,
            abbreviation TEXT,
            address TEXT,
            phone TEXT,
            representative TEXT,
            status TEXT,
            activity_date TEXT,
            tax_office TEXT,
            company_type TEXT,
            main_business TEXT,
            last_updated TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_company(self, company):
        query = """
        INSERT OR IGNORE INTO companies (
            name, tax_id, abbreviation, address, phone, representative, status,
            activity_date, tax_office, company_type, main_business, last_updated
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        values = (
            company.get("name", ""),
            company.get("tax_id", ""),
            company.get("abbreviation", ""),
            company.get("address", ""),
            company.get("phone", ""),
            company.get("representative", ""),
            company.get("status", ""),
            company.get("activity_date", ""),
            company.get("tax_office", ""),
            company.get("company_type", ""),
            company.get("main_business", ""),
            company.get("last_updated", "")
        )
        self.conn.execute(query, values)
        self.conn.commit()
# Trong database_handler.py, thêm phương thức cập nhật trạng thái cào:
    def update_scraping_status(self, last_page):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO scraping_status (id, last_page) VALUES (1, ?)", (last_page,))
        self.conn.commit()

    def get_last_scraping_status(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT last_page FROM scraping_status WHERE id = 1")
        result = cursor.fetchone()
        return result[0] if result else 1  # Nếu không tìm thấy, bắt đầu từ trang 1

    def close(self):
        self.conn.close()
