import json
import os
from flask import Flask, redirect, request, url_for, abort, jsonify
from src.model.users_repo import UsersRepo
from src.model.pets_repo import PetsRepo
from src.model.posts_repo import PostsRepo
from src.model.models import User, Post, Pet

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Login
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

repo = UsersRepo()
client = WebApplicationClient(GOOGLE_CLIENT_ID)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return repo.get_user(user_id)

# Temp landing page 
@app.route("/")
def index():
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
        repo.set_user_active(user.id)
    user = repo.get_user(unique_id)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    repo.set_user_inactive(current_user.id)
    logout_user()
    return redirect(url_for("index"))

@app.route("/posts", methods = ["POST"])
def createNewPost():
    petId = request.form["petId"]
    message = request.form["message"]
    repo.create_post(petId, message)
    # TODO Finish success
    return redirect(url_for('success'))

# Posts
posts_repo = PostsRepo()
@app.route('/posts', methods=['POST'], defaults={'postId':None})
@app.route('/posts/<postId>', methods=['GET','DELETE'])
def posts(postId):
    try:
        if request.method == 'GET': 
            post = posts_repo.get_post(postId)
            if not post:
                return abort(404)
            return json.dumps(post, indent=4, sort_keys=True, default=str)
        elif request.method == 'POST':
            # need validation
            post = Post.from_dict(request.get_json())
            posts_repo.create_post(post)
            return json.dumps(post, indent=4, sort_keys=True, default=str)
        elif request.method == 'DELETE':
            delete = posts_repo.delete_post(postId)
            if not delete:
                return abort(404)
            return ('', 204)
    except Exception as e:
        abort(500, {'message': str(e)})

# Friends
@app.route("/friends/<petId>/posts", methods = ["GET"])
def friendPosts(petId):
    try:
        posts = posts_repo.get_friend_posts(petId)
        return json.dumps(posts, indent=4, sort_keys=True, default=str)
    except Exception as e:
        abort(500, {'message': str(e)})

# Pets
@app.route("/pets/<petId>/posts", methods = ["GET"])
def petPosts(petId):
    try:
        posts = posts_repo.get_pet_posts(petId)
        return json.dumps(posts, indent=4, sort_keys=True, default=str)
    except Exception as e:
        abort(500, {'message': str(e)})

pets_repo = PetsRepo()
@app.route('/pets', methods=['GET','POST'], defaults={'petId':None})
@app.route('/pets/<petId>', methods=['GET','PUT','DELETE'])
def pets(petId):
    try:
        if request.method == 'GET': 
            if petId:
                pet = pets_repo.get_pet(petId)
                if not pet:
                    return abort(404)
                return json.dumps(pet, indent=4, sort_keys=True, default=str)
            else:
                pets = pets_repo.get_pets()
                return json.dumps(pets, indent=4, sort_keys=True, default=str)
        elif request.method == 'POST':
            # need validation
            pet = Pet.from_dict(request.get_json())
            pets_repo.create_pet(pet)
            return json.dumps(pet, indent=4, sort_keys=True, default=str)
        elif request.method == 'PUT':
            pet = Pet.from_dict(request.get_json())
            # need validation
            if pet.id != petId:
                return abort(400)
            update = pets_repo.update_pet(pet)
            if not update:
                return abort(404)
            return json.dumps(update, indent=4, sort_keys=True, default=str)
        elif request.method == 'DELETE':
            delete = pets_repo.delete_pet(petId)
            if not delete:
                return abort(404)
            return ('', 204)
    except Exception as e:
        abort(500, {'message': str(e)})

if __name__ == "__main__":
    app.run(ssl_context=('adhoc'))