from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
import os

app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    "client_secret.json",
    scopes=["https://www.googleapis.com/auth/drive.file"],
    redirect_uri="https://feifei.kaven.railway.app/oauth2callback"
)

@app.route("/auth")
def auth():
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)

@app.route("/oauth2callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    return "授权成功！"

@app.route("/")
def home():
    return "欢迎来到妃妃记忆系统 - 授权请访问 /auth"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
