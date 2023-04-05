import json
import os
from flask import Flask, redirect, request, url_for, jsonify
from src.model.repo import PostgresRepo
from src.model.models import User

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
import requests

# These need to be added as environment variables on your local machine
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

repo = PostgresRepo()


@login_manager.user_loader
def load_user(user_id):
    return repo.get_user(user_id)

# Temp landing page 
@app.route("/")
def index():
    print(current_user)
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

# Utility method to get Google SSO endpoint information
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get the code from the querystring
    code = request.args.get("code")

    # Find the token issuer endpoint
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Get token via code
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    # Hit user info endpoint
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = repo.get_user(unique_id)
    if not user:
        user = User(id=unique_id, name=users_name, email=users_email, is_active=True, is_authenticated=True)
        repo.create_user(user)
    else:
        repo.set_active(user.id)
    user = repo.get_user(unique_id)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    repo.set_inactive(current_user.id)
    logout_user()
    return redirect(url_for("index"))

@app.route("/posts", methods = ["POST"])
def createNewPost():
    petId = request.form["petId"]
    message = request.form["message"]
    repo.create_post(petId, message)
    # TODO Finish success
    return redirect(url_for('success'))

@app.route("/posts/friends/<petId>", methods = ["GET"])
def getFriendsPosts(petId):
    posts = repo.get_friend_posts(petId)
    return json.dumps(posts, indent=4, sort_keys=True, default=str)

@app.route("/posts/<postId>", methods = ["GET"])
def getPost(postId):
    post = repo.get_post(postId)
    return json.dumps(post, indent=4, sort_keys=True, default=str)

@app.route("/posts/<postId>", methods = ["DELETE"])
def deletePost(postId):
    post = repo.delete_post(postId)
    return redirect(url_for('success'))

@app.route("/posts/pet/<petId>", methods = ["GET"])
def getAllPetPosts(petId):
    posts = repo.get_posts(petId)
    return json.dumps(posts, indent=4, sort_keys=True, default=str)

@app.route("/friends/<petId>", methods = ["GET"])
def getFriends(petId):
    friends = repo.get_friends(petId)
    return json.dumps(friends, indent=4, sort_keys=True, default=str)

@app.route("/nonfriends/<petId>", methods = ["GET"])
def getNonFriends(petId):
    nonFriends = repo.get_non_friends(petId)
    return json.dumps(nonFriends, indent=4, sort_keys=True, default=str)

if __name__ == "__main__":
    app.run(ssl_context=('adhoc'))