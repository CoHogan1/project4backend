import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


player = Blueprint('users', 'player') # doubble check the db name

#     /api/v1/player

# index
@player.route('/', methods=['GET'])
def player_index():
    if current_user.is_authenticated:
        player_dic = [model_to_dict(play) for play in current_user.my_player]

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
@player.route('/', methods=['POST'])
@login_required
def create_dog():
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
@player.route('/<id>', methods=['GET'])
def get_one_player(id):
    print('get_one_player route accessed')
    player = models.Users.get_by_id(id)
    return  jsonify(
        data = model_to_dict(player),
        message = "Found user",
        status = 200
    ), 200


#update
@player.route('/<id>', methods=["PUT"])
def update_player(id):
    print("Update route hit")
    payload = request.get_json()
    models.User.update(**payload).where(models.User.id==id).execute()

    return jsonify(
        data = model_to_dict(models.User.get_by_id(id)),
        status = 200,
        message = "Updated player"
    ), 200


# Delete
@player.route('/<id>', methods=['DELETE'])
def delete_player(id):
    print("Del route hit")
    models.User.delete().where(models.User.id==id).execute()

    return jsonify(
        data = "Deleted player",
        status = 200,
        message = "Yeet that player.",
    ), 200
