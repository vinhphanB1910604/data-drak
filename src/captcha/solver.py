# src/captcha/solver.py

import requests

class CaptchaSolver:
    def __init__(self, api_key):
        self.api_key = api_key

    def solve_captcha(self, captcha_image_url):
        # Giải captcha qua 2Captcha API
        response = requests.post(
            "http://2captcha.com/in.php", 
            data={
                'key': self.api_key,
                'method': 'base64',
                'body': captcha_image_url,  # Truyền dữ liệu captcha (ở dạng base64 hoặc URL)
                'json': 1,
            }
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                return data['request']  # Trả về mã captcha đã giải
            else:
                raise Exception("Captcha solving failed")
        else:
            raise Exception("Failed to connect to 2Captcha API")
