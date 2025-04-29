from flask import Flask, jsonify, request
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.scraper.my_target_scraper import MyTargetScraper

app = Flask(__name__)

# Giới hạn tối đa concurrent scraping
MAX_WORKERS = 7
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

@app.route("/scrape", methods=["POST"])
def scrape():
    """
    POST /scrape
    {
      "page": 1           # optional, nếu bạn chỉ muốn cào một page cụ thể
    }
    """
    data = request.get_json(silent=True) or {}
    page = data.get("page", None)

    def task(p):
        scraper = MyTargetScraper()
        # Nếu có page cụ thể, chỉ cào page đó; nếu không, cào pagination đầy đủ:
        if p:
            url = f"{scraper.base_url}?page={p}"
            html = scraper.send_request(url)
            batch = scraper.parse_company_data(html) if html else []
            return {"page": p, "data": batch}
        else:
            # full pagination
            scraper.start()  # dùng start() để tự detect & lưu vào DB
            return {"message": "Done full pagination"}

    # Gửi vào pool
    future = executor.submit(task, page)
    result = future.result()   # vì client đang chờ đồng bộ; nếu muốn async, trả URL job ID

    return jsonify(result), 200

if __name__ == "__main__":
    # Chạy local dev: threaded=True cho phép multi-request song song
    app.run(host="0.0.0.0", port=8000, threaded=True)
