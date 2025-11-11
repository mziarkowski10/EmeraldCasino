from flask import request, jsonify, Blueprint
from db import connect_db, create_db, add_player, player_exists, get_player, update_balance

routes = Blueprint("routes", __name__)

@routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")

    if player_exists(username):
        return jsonify({
            "success": False,
            "message": "Username already taken",
            "username": username
        })

    if not username:
        return jsonify({
            "success": False,
            "message": "Username is required"
        })

    add_player(username)

    return jsonify({
        "success": True,
        "message": "Player registered successfully",
        "player": {
            "username": username,
            "balance": get_player(username).get("balance"),
            "created_at": get_player(username).get("created_at")
        }
    })

@routes.route("/login", methods=["POST"])
def login():
    pass