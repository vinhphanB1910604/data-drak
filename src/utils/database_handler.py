import sqlite3

class DatabaseHandler:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tax_id TEXT,
            abbreviation TEXT,
            address TEXT,
            phone TEXT,
            representative TEXT,
            status TEXT
        )
        """)
        self.connection.commit()

    def insert_company(self, company):
        sql = """
        INSERT INTO companies (name, tax_id, abbreviation, address, phone, representative, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        vals = (
            company["name"], company["tax_id"], company["abbreviation"],
            company["address"], company["phone"],
            company["representative"], company["status"]
        )
        try:
            self.cursor.execute(sql, vals)
            self.connection.commit()
        except Exception as e:
            print(f"[DB ERROR] {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()
