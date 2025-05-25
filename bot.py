
from flask import Flask, request, send_file

from flask import Flask, request, jsonify

# Telegram API credentials

flask_app = Flask(__name__)

@flask_app.route('/result')
def get_result():
    roll_no = request.args.get('roll_no')
    url = request.args.get('url')
    if not roll_no:
        return "Error: roll_no parameter missing.", 400

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://rajeduboard.rajasthan.gov.in/RESULT2022/SEV/SEVROLL_INPUT.ASP',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
    }
    data = {
        'roll_no': roll_no
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}", 500

@flask_app.route('/')
def home():
    return " Board Results Apis Are Working Well"





if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
