from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route('/')
def home():
    return "Board Results APIs are working well."

BOT_TOKEN = '7831738668:AAH7Qc1zYoNd5DrY85kU4EN4GXY01JF91fk'

@app.route('/resultsend')
def send_result_pdf_direct():
    user_id = request.args.get('user_id')
    roll_no = request.args.get('roll_no')
    full_query = request.query_string.decode('utf-8')

    sourceurl_pos = full_query.find('sourceurl=')
    sourceurl = full_query[sourceurl_pos + 10:] if sourceurl_pos != -1 else None

    if not user_id or not roll_no or not sourceurl:
        return "Missing parameters", 400

    # Final PDF URL to be sent directly
    encoded_sourceurl = requests.utils.quote(sourceurl, safe='')
    pdf_url = f"https://sainipankaj12.serv00.net/savepdf.php?url=https://sainipankaj12.serv00.net/Result/get.php?roll_no={roll_no}&url={encoded_sourceurl}"

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    payload = {
        'chat_id': user_id,
        'document': pdf_url,
        'caption': f"Your result PDF for Roll No: {roll_no}"
    }

    try:
        telegram_response = requests.post(telegram_url, data=payload)
        if telegram_response.status_code == 200:
            return "Success", 200
        else:
            return f"Failed to send PDF. Telegram status: {telegram_response.status_code}", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/result')
def get_result():
    roll_no = request.args.get('roll_no')
    url = request.args.get('url')

    if not roll_no or not url:
        return jsonify({'error': 'Missing roll_no or url parameter.'}), 400

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://rajeduboard.rajasthan.gov.in/RESULT2022/SEV/SEVROLL_INPUT.ASP',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
    }

    try:
        response = requests.post(url, headers=headers, data={'roll_no': roll_no}, timeout=10)
        return response.text, response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500


@app.route('/result-1')
def result_page():
    name = request.args.get('name')
    page = request.args.get('page', '1')
    url = request.args.get('url')
    user_id = request.args.get('user_id', '')

    if not name or not url:
        return "Missing 'name' or 'url' parameter", 400

    session = requests.Session()
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        initial_response = session.post(url, headers=headers, data={'name': name})
        soup = BeautifulSoup(initial_response.text, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value', '')
        viewstategen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value', '')
    except Exception as e:
        return f"Failed to fetch initial page: {str(e)}", 500

    post_data = {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategen,
        '__EVENTTARGET': 'GridView1',
        '__EVENTARGUMENT': f'Page${page}',
        'name': name
    }

    try:
        final_response = session.post(url, headers=headers, data=post_data)
        soup = BeautifulSoup(final_response.text, 'html.parser')
        table = soup.find('table', {'id': 'GridView1'})
        if not table:
            return "No result table found.", 400

        result_link = url.replace("mName-results.aspx", "mrollresult.asp").replace("mname-results.aspx", "mrollresult.asp")

        table_html = str(table)
        table_html = table_html.replace("__doPostBack", "openlink")
        table_html = table_html.replace("showresult('", "showresult('").replace("')", "', this)")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{name}</title>
            <style>
                body {{ zoom: 87%; background-color: #fff; color: #000; margin: 0; padding: 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ padding: 8px; border: 1px solid #ccc; text-align: center; }}
                th {{ background: #eee; }}
            </style>
            <script>
                function openlink(control, arg) {{
                    const parts = arg.split('$');
                    if (parts.length === 2 && parts[0] === 'Page') {{
                        const page = parts[1];
                        const name = encodeURIComponent("{name}");
                        const url = encodeURIComponent("{url}");
                        const user_id = "{user_id}";
                        window.location.href = "/result-1?user_id=" + user_id + "&name=" + name + "&page=" + page + "&url=" + url;
                    }}
                }}

                function showresult(roll_no, btn) {{
                    const result_link = "{result_link}";
                    const user_id = "{user_id}";
                    if (!user_id) {{
                        alert("Telegram user ID not found.");
                        return;
                    }}

                    btn.disabled = true;
                    btn.value = "Please wait...";

                    const fetch_url = "/resultsend?user_id=" + user_id + "&roll_no=" + encodeURIComponent(roll_no) + "&sourceurl=" + encodeURIComponent(result_link);
                    fetch(fetch_url).then(response => {{
                        if (response.status === 200) {{
                            alert("Sent to Telegram. Please check Telegram.");
                        }} else {{
                            alert("Failed to send result. Status: " + response.status);
                        }}
                    }}).catch(error => {{
                        console.error("Error:", error);
                        alert("An error occurred while sending the result.");
                    }}).finally(() => {{
                        btn.disabled = false;
                        btn.value = "Get";
                    }});
                }}
            </script>
        </head>
        <body>
            <div style="display: flex; align-items: center; gap: 10px; padding: 10px;">
                <button onclick="history.back()" style="background: none; border: none; cursor: pointer;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="#007bff" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M15 8a.5.5 0 0 1-.5.5H2.707l4.147 4.146a.5.5 0 0 1-.708.708l-5-5a.5.5 0 0 1 0-.708l5-5a.5.5 0 1 1 .708.708L2.707 7.5H14.5A.5.5 0 0 1 15 8z"/>
                    </svg>
                </button>
                <h2 style="margin: 0;">{name}</h2>
            </div>
            {table_html}
        </body>
        </html>
        """
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        return response

    except Exception as e:
        return f"Error while processing result table: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
