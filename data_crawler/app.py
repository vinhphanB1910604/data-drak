from flask import Flask, render_template, request, redirect, url_for
from src.scraper.my_target_scraper import MyTargetScraper  # Import class MyTargetScraper
import threading

app = Flask(__name__)

# Hàm để chạy quá trình cào dữ liệu trong background
def run_scraper(url):
    scraper = MyTargetScraper()
    scraper.base_url = url  # Đặt URL cào từ frontend
    scraper.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            # Khởi tạo một luồng để cào dữ liệu mà không làm gián đoạn ứng dụng web
            threading.Thread(target=run_scraper, args=(url,)).start()
            return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
