from flask import Flask, request, redirect, session, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
DISCORD_API_BASE_URL = 'https://discord.com/api'
OAUTH2_TOKEN_URL = f'{DISCORD_API_BASE_URL}/oauth2/token'
OAUTH2_AUTHORIZE_URL = f'{DISCORD_API_BASE_URL}/oauth2/authorize'

@app.route('/')
def home():
    return 'Welcome to the OAuth2 example. Go to /login to start'

@app.route('/login')
def login():
    discord_login_url = f"{OAUTH2_AUTHORIZE_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=coded&scope=identify"
    return redirect(discord_login_url)

@app.route('callback')
def outah_callback():
    code = request.args.get('code')
    if code is None:
        return 'Authorization failed.', 400
    
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(OAUTH2_TOKEN_URL, data=data, headers=headers)
    response_data = response.json()

    if 'access_token' not in response_data:
        return 'Failed to get access token', 400
    
    access_token = response_data['access_token']
    session['access_token'] = access_token

    return 'OAuth2 flow complete. You can now use the bot.'

if __name__ == '__main__':
    app.run(port=3000)