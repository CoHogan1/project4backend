import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user

from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


users = Blueprint('users','users')


# /api/v1/users

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
@users.route('/logout', methods=['GET','DELETE'])
def logout():
    logout_user()
    print("Logged out!!!!!")

    return jsonify(
        data={},
        status=200,
        message='User Successfully logout'
    ), 200


# here====================================================

@users.route('/', methods=['GET'])
def player_index():
    print("index")
    if current_user.is_authenticated:
        result = models.User.select()
        player_dic = [model_to_dict(play) for play in result]

        return jsonify({
            'data': player_dic,
            'message': f"Found {len(player_dic)} users",
            'status': 200
        }), 200
    else:
        player_dic = [model_to_dict(play) for play in models.User.select()]
        return jsonify({
            'data': player_dic,
            'message': f"Successfully found {len(player_dic)} users",
            'status': 200
        }), 200


# create
@users.route('/', methods=['POST'])
@login_required
def create_dog():
    print('create')
    payload = request.get_json()
    new_player = models.User.create(name=payload['name'],email=payload['email'],username=payload['username'])
    print(new_player)
    player_dic = model_to_dict(new_player)
    return jsonify(
        data=player_dic,
        message="Success created player",
        status=201
    ), 201

#show
@users.route('/<id>', methods=['GET'])
def get_one_player(id):
    print("show")
    print('get_one_player route accessed')
    player = models.User.get_by_id(id)
    return  jsonify(
        data = model_to_dict(player),
        message = "Found user",
        status = 200
    ), 200


#update
@users.route('/<id>', methods=["PUT"])
def update_player(id):
    print("Update route hit")
    payload = request.get_json()
    print(payload)

    models.User.update(**payload).where(models.User.id==id).execute()

    return jsonify(
        data = model_to_dict(models.User.get_by_id(id)),
        status = 200,
        message = "Updated player"
    ), 200


# Delete
@users.route('/<id>', methods=['DELETE'])
def delete_player(id):
    print("Del route hit")
    models.User.delete().where(models.User.id==id).execute()

    return jsonify(
        data = "Deleted player",
        status = 200,
        message = "Yeet that player.",
    ), 200
