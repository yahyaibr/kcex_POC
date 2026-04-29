import os
import requests
from flask import Flask, redirect, jsonify

app = Flask(__name__)

# The target API URL
API_URL = "https://www.kcex.com/uc/user_api/sns/x/config"

# Headers and Cookies from your original request
HEADERS = {
    "Host": "www.kcex.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Accept": "*/*",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.kcex.com/user",
    "Language": "en-US",
    "Accept-Timezone": "UTC+01:00",
    "Authorization": "WEB0f1dd244bebc495401ff81434520e2caafcb988e1b2792acd85b573b4ff9f44c",
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
    "Authorization": "WEB0f1dd244bebc495401ff81434520e2caafcb988e1b2792acd85b573b4ff9f44c",
    "kcex_exchange_order_confirmation": "[1,2,3,4,5,100,101,\"FOLLOW_LIMIT_ORDER\"]"
}

@app.route('/')
def health_check():
    return "Server is running. Use /start-auth to initiate the request."

@app.route('/start-auth')
def start_auth():
    # Parameters provided in your original GET request
    params = {
        'callback': 'https://www.kcex.com/auth/callback?redirect=https://webhook.site/5a042f89-c5cf-4180-8903-7a5b65a4455f'
    }

    try:
        # Make the request to KCEX
        # timeout=10 prevents the app from hanging forever if KCEX is slow
        response = requests.get(API_URL, headers=HEADERS, cookies=COOKIES, params=params, timeout=10)
        
        # Check if the response was successful
        if response.status_code == 200:
            json_data = response.json()
            
            # Extract the Twitter authorization URL
            twitter_url = json_data.get("data")
            
            if twitter_url:
                # Redirect the actual user to Twitter
                return redirect(twitter_url)
            else:
                return jsonify({"error": "Twitter URL not found in response", "raw_body": json_data}), 500
        else:
            return jsonify({
                "error": "KCEX API returned an error status",
                "status_code": response.status_code,
                "content": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"error": "Internal server error during request", "message": str(e)}), 500

if __name__ == '__main__':
    # Railway provides the PORT environment variable. 
    # We must bind to 0.0.0.0 to be accessible externally.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
