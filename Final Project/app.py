import time
import json
import os
from flask import Flask, redirect, request, url_for, abort, jsonify, make_response, render_template
from model.users_repo import UsersRepo
from model.pets_repo import PetsRepo
from model.posts_repo import PostsRepo
from model.friends_repo import FriendsRepo
from model.reactions_repo import ReactionsRepo
from model.models import User, Post, Pet, Friend, Reaction
import time
from flask_cors import CORS

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
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config["IMAGE_UPLOADS"] = ".\photos"

# Login
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration")

repo = UsersRepo()
client = WebApplicationClient(GOOGLE_CLIENT_ID)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return repo.get_user(user_id)

# Temp landing page
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/")
def index():
    if not current_user or not current_user.is_active:
        return redirect('/signin')

    user = load_user(current_user.id)
    pets = pets_repo.get_user_pets(user.id)
    if not pets:
        return redirect('/getstarted')
    
    return render_template('index.html', user = user.name)

@app.route("/getstarted")
@login_required
def get_started():
    user = load_user(current_user.id)
    pets = pets_repo.get_user_pets(user.id)
    # If they already have pets set up, just go to their feed
    if pets:
        redirect('/')
    return render_template('getstarted.html', user = user.name)

@app.route("/signin")
def signin():
    return render_template('signin.html')

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
        user = User(id=unique_id, name=users_name, email=users_email,
                    is_active=True, is_authenticated=True)
        repo.create_user(user)
    else:
        repo.set_user_active(user.id)
    user = repo.get_user(unique_id)

    # Begin user session by logging the user in
    login_user(user, remember=True)

    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    repo.set_user_inactive(current_user.id)
    logout_user()
    return redirect("/")


# Posts
posts_repo = PostsRepo()


@app.route('/posts', methods=['POST'], defaults={'postId': None})
@app.route('/posts/<postId>', methods=['GET', 'DELETE'])
def posts(postId):
    try:
        if request.method == 'GET':
            post = posts_repo.get_post(postId)
            if not post:
                return abort(404)
            return jsonify(post)
        elif request.method == 'POST':
            # need validation
            post = Post.from_dict(request.get_json())
            posts_repo.create_post(post)
            return jsonify(posts_repo.get_post(post.id))
        elif request.method == 'DELETE':
            delete = posts_repo.delete_post(postId)
            if not delete:
                return abort(404)
            return ('', 204)
    except Exception as e:
        abort(500, {'message': str(e)})


@app.route('/posts/<postId>/photos', methods=['POST'])
def createPostPhotos(postId):
    try:
        if request.files:
            post = posts_repo.get_post_object(postId)
            if not post:
                return abort(404)

            response = upload_photo(request, postId, 'post')
            post.photo = response['filenames'][0]
            posts_repo.update_post(post)

            return jsonify(response)
        abort(400)
    except Exception as e:
        abort(500, {'message': str(e)})

# Friends


@app.route("/friends/<petId>/posts", methods=["GET"])
def friendPosts(petId):
    try:
        posts = posts_repo.get_friend_posts(petId)
        return jsonify(posts)
    except Exception as e:
        abort(500, {'message': str(e)})


friends_repo = FriendsRepo()


@app.route("/friends/<petId>", methods=["GET"])
def getFriends(petId):
    friends = friends_repo.get_friends(petId)
    return jsonify(friends)


@app.route("/nonfriends/<petId>", methods=["GET"])
def getNonFriends(petId):
    nonFriends = friends_repo.get_non_friends(petId)
    return json.dumps(nonFriends, indent=4, sort_keys=True, default=str)


@app.route("/friends", methods=["POST"])
def createFriend():
    friend = Friend.from_dict(request.get_json())
    friends_repo.add_friend(friend)
    return jsonify(friends_repo.get_friends(friend.pet_id))
    
    


@app.route("/friends/<id>", methods=["DELETE"])
def removeFriend(id):
    delete = friends_repo.delete_friend(id)
    if not delete:
        return abort(404)
    return ('', 204)

# Pets


@app.route("/pets/<petId>/posts", methods=["GET"])
def petPosts(petId):
    try:
        posts = posts_repo.get_pet_posts(petId)
        return jsonify(posts)
    except Exception as e:
        abort(500, {'message': str(e)})


pets_repo = PetsRepo()


@app.route('/pets', methods=['GET', 'POST'], defaults={'petId': None})
@app.route('/pets/<petId>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def pets(petId):
    try:
        if request.method == 'GET':
            if petId:
                pet = pets_repo.get_pet(petId)
                if not pet:
                    return abort(404)
                return jsonify(pet)
            else:
                pets = pets_repo.get_pets()
                return jsonify(pets)
        elif request.method == 'POST':
            # need validation
            pet = request.get_json()
            pet['user_id'] = current_user.id
            pet_obj = Pet.from_dict(pet)
            pets_repo.create_pet(pet_obj)
            return jsonify(pets_repo.get_pet(pet_obj.id))
        elif request.method == 'PUT':
            pet = Pet.from_dict(request.get_json())
            # need validation
            if pet.id != petId:
                return abort(400)
            update = pets_repo.update_pet(pet)
            if not update:
                return abort(404)
            return jsonify(update)
        elif request.method == 'DELETE':
            delete = pets_repo.delete_pet(petId)
            if not delete:
                return abort(404)
            return ('', 204)
    except Exception as e:
        abort(500, {'message': str(e)})


@app.route('/pets/<petId>/photos', methods=['GET', 'POST'])
def petPhotos(petId):
    try:
        if request.method == 'GET':
            pet = pets_repo.get_pet(petId)
            if not pet:
                abort(404)
            return jsonify(make_photo_response(pet.id, pet.pics))
        elif request.method == 'POST':
            pet = pets_repo.get_pet(petId)
            if not pet:
                abort(404)
            if request.files:
                response = upload_photo(request, petId, 'pet')
                pets_repo.add_pet_photo(petId, response['filenames'][0])
                return jsonify(response)
            abort(400)
    except Exception as e:
        abort(500, {'message': str(e)})


@app.route('/pets/<petId>/photos/<filename>', methods=['DELETE'])
def deletePetPhotos(petId, filename):
    try:
        pet = pets_repo.get_pet(petId)
        if not pet:
            abort(404)
        deleted = pets_repo.delete_pet_photo(petId, filename)
        if not deleted:
            abort(400)
        os.remove(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        return ('', 204)
    except Exception as e:
        abort(500, {'message': str(e)})


def upload_photo(request, resourceId, resourceType):
    ts = time.strftime("%Y%m%d-%H%M%S")
    image = request.files["file"]
    filename = resourceId + '-' + ts + '-' + resourceType + '-' + image.filename
    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
    return make_photo_response(resourceId, [filename])


def make_photo_response(resourceId, filenames):
    return {'resourceId': resourceId, 'filenames': filenames}


# Reactions
reactions_repo = ReactionsRepo()


@app.route("/reactions/<postId>", methods=["GET"])
def get_post_reactions(postId):
    reactions = reactions_repo.get_post_reactions(postId)
    return jsonify(reactions)


@app.route("/reactions/treats/<postId>", methods=["GET"])
def get_post_treats(postId):
    treats = reactions_repo.get_post_treats(postId)
    return jsonify(treats)

@app.route("/reactions/comments/<postId>", methods = ["GET"])
def get_post_comments(postId):
    comments = reactions_repo.get_post_comments(postId)
    return jsonify(comments)

@app.route("/reactions", methods = ["POST"])
def createReaction():
    reaction = Reaction.from_dict(request.get_json())
    reactions_repo.create_post_reaction(reaction)
    return jsonify(reactions_repo.get_post_reactions(reaction.post_id))

@app.route("/reactions/<reactionId>", methods = ["DELETE"])
def removeReaction(reactionId):
    delete = reactions_repo.delete_post_reaction(reactionId)
    if not delete:
        return abort(404)
    return ('', 204)


if __name__ == "__main__":
    app.run(ssl_context=('adhoc'))