import requests
from flask import Flask, redirect, render_template_string

app = Flask(__name__)

# The target API URL
API_URL = "https://www.kcex.com/uc/user_api/sns/x/config"

# Headers exactly as provided in your request
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

# Cookies from your request
COOKIES = {
    "NEXT_LOCALE": "en-US",
    "kcex_base_fiat": "USD",
    "_ga": "GA1.1.1270344583.1773584302",
    "Authorization": "WEB0f1dd244bebc495401ff81434520e2caafcb988e1b2792acd85b573b4ff9f44c",
    "kcex_exchange_order_confirmation": "[1,2,3,4,5,100,101,\"FOLLOW_LIMIT_ORDER\"]"
}

@app.route('/start-auth')
def start_auth():
    # 1. Prepare the query parameters (the 'callback' part)
    params = {
        'callback': 'https://www.kcex.com/auth/callback?redirect=https://webhook.site/5a042f89-c5cf-4180-8903-7a5b65a4455f'
    }

    try:
        # 2. Perform the GET request to the KCEX API
        response = requests.get(API_URL, headers=HEADERS, cookies=COOKIES, params=params)
        
        if response.status_code == 200:
            data_json = response.json()
            
            # 3. Extract the Twitter URL from the response
            # Based on your example: {"code":0, "data":"https://api.twitter.com/..."}
            redirect_url = data_json.get("data")
            
            if redirect_url:
                # 4. Redirect the user's browser to the Twitter OAuth page
                return redirect(redirect_url)
            else:
                return "Error: No redirect URL found in response data.", 500
        else:
            return f"Error: API returned status {response.status_code}", response.status_code

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    # Run the Flask app
    print("Go to http://127.0.0.1:5000/start-auth to begin.")
    app.run(debug=True, port=5000)
