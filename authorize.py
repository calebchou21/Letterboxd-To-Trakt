import http.server
import socketserver
import webbrowser
import threading
import secrets
import time
import requests

from urllib.parse import urlparse, urlencode, parse_qs, quote

CLIENT_ID = ""
CLIENT_SECRET = ""

TRAKT_AUTHORIZATION_URL = "https://trakt.tv/oauth/authorize"
TRAKT_TOKEN_URL = "https://trakt.tv/oauth/token"
TOKEN_URL = "https://api.trakt.tv/oauth/token"
REDIRECT_URI = "http://localhost:12345/callback"

class NoAuthorizationCodeError(Exception):
    pass

class AccessTokenError(Exception):
    pass

def generate_state():
    return secrets.token_urlsafe(16)

def exchange_code_for_token(authorization_code):
    token_data = {
        'code': authorization_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(TRAKT_TOKEN_URL, data=token_data)
    token_json = response.json()

    if 'access_token' in token_json:
        access_token = token_json['access_token']
        print(f"Access Token: {access_token}")
        return access_token
    else:
        raise AccessTokenError(f"Failed to obtain access token. Response: {token_json}")

def authorize():
    callback_server = start_callback_server()
    state = generate_state()
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state
    }
    encoded_params = urlencode(params, quote_via=quote)
    try:
        authorization_endpoint = f"{TRAKT_AUTHORIZATION_URL}?{encoded_params}"
        webbrowser.open_new_tab(authorization_endpoint)
        time.sleep(5)
        authorization_code = callback_server.authorization_code
        callback_server.shutdown()
        callback_server.server_close()
    except NoAuthorizationCodeError as e:
        print(e)

    try:
        access_token = exchange_code_for_token(authorization_code)
        return access_token
    except AccessTokenError as e:
        print(e)

class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        query_parameters = parse_qs(urlparse(self.path).query)

        if self.path.startswith('/callback'):
            query_parameters = parse_qs(urlparse(self.path).query)
            if 'code' in query_parameters:
                self.server.authorization_code = query_parameters['code'][0]
                print(f"Authorization code: {self.server.authorization_code}")
            else:
                raise NoAuthorizationCodeError("No authorization code found.")

def start_callback_server():
    server = socketserver.TCPServer(("localhost", 12345), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server   


