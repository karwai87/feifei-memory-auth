from flask import Flask, redirect, request, session
from google_auth_oauthlib.flow import Flow
import os
from flask_session import Session  # 需要安装flask-session

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

if os.environ.get("FLASK_ENV") == "development":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
REDIRECT_URI = "https://feifei.kaven.railway.app/oauth2callback"

@app.route("/auth")
def auth():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route("/oauth2callback")
def callback():
    state = session.get('state')
    if state != request.args.get('state'):
        return "State参数不匹配，可能遭受CSRF攻击", 400

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    try:
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        return "授权成功！您现在可以关闭此页面。"
    except Exception as e:
        return f"授权失败: {str(e)}"

@app.route("/")
def home():
    return "欢迎来到妃妃记忆系统 - 授权请访问 /auth"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)