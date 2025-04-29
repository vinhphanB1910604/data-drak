import sqlite3
import pandas as pd
import re

# Kết nối database
conn = sqlite3.connect('data-grak.db')
cursor = conn.cursor()

# Đọc toàn bộ dữ liệu trong bảng companies
cursor.execute('SELECT name, tax_id, abbreviation, address, phone, representative, status, created_at FROM companies')
rows = cursor.fetchall()

# Đóng kết nối
conn.close()

# Làm sạch từng dòng dữ liệu
def clean_text(text):
    if text is None:
        return ""
    # Xóa ký tự lạ như � hoặc kí tự không in được
    text = re.sub(r'[^\x00-\x7F\u00A0-\uFFFF]+', '', text)
    # Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    return text

cleaned_rows = []
for row in rows:
    cleaned_row = [clean_text(str(field)) for field in row]
    cleaned_rows.append(cleaned_row)

# Đưa vào DataFrame
columns = ["Tên công ty", "Mã số thuế", "Tên viết tắt", "Địa chỉ", "Điện thoại", "Người đại diện", "Tình trạng", "Ngày tạo"]
df = pd.DataFrame(cleaned_rows, columns=columns)

# Ghi ra Excel
output_file = "output.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Đã xuất dữ liệu sạch ra file: {output_file}")
