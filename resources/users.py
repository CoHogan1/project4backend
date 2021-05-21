import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user

users = Blueprint('users','users')

@users.route('/', methods=['GET'])
def test_user_resource():
    return "Users route working all users"

#register
@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()

    print(payload, " this is what was registered")
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(
            data={},
            message=f"A user with the email {payload['email']} already exists",
            status=401
        ), 401
    except models.DoesNotExist: # except is like a catch in JS
        pw_hash = generate_password_hash(payload['password'])
        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )
        print(created_user)
        login_user(created_user)
        created_user_dict = model_to_dict(created_user)
        print(created_user_dict)
        print(type(created_user_dict['password']))
        created_user_dict.pop('password')
        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user {created_user_dict['email']}",
            status=201
        ), 201

#login
@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        password_is_good = check_password_hash(user_dict['password'], payload['password'])
        if (password_is_good):
            login_user(user) # in express we did this manually by setting stuff in session
            user_dict.pop('password')
            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['email']}",
                status=200
            ), 200
        else:
            print('pw is no good')
            return jsonify(
                data={},
                message="Email or password is incorrect", # let's be vague
                status=401
            ), 401
    except models.DoesNotExist:
        print('username is no good')
        return jsonify(
            data={},
            message="Email or password is incorrect", # let's be vague
            status=401
        ), 401

#logout route
@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    print("Loggedout")

    return jsonify(
        data={},
        status=200,
        message='User Successfully logout'
    ), 200



# checking to see if this is a different color.
