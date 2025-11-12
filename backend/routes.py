from flask import request, jsonify, Blueprint
from db import connect_db, create_db, add_player, player_exists, get_player, change_balance

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
    data = request.get_json()
    username = data.get("username")

    if not player_exists(username):
        return jsonify({
            "success": False,
            "message": "Player not found",
            "username": username
        })

    user_data = get_player(username)
    user_data["success"] = True
    user_data["message"] = "Login successful"

    return jsonify(user_data)

@routes.route("/update_balance", methods=["POST"])
def update_balance():
    data = request.get_json()
    username, amount = data.get("username"), data.get("amount")

    if not player_exists(username):
        return jsonify({
            "success": False,
            "message": "Player does not exist",
            "username": username
        })

    res = change_balance(username, amount)

    return jsonify(res)

@routes.route("/balance", methods=["POST"])
def balance():
    data = request.get_json()
    username = data.get("username")

    if not player_exists(username):
        return jsonify({
            "success": False,
            "message": "Player does not exist",
            "username": username
        })

    user_data = get_player(username)
    balance = user_data.get("balance")

    return jsonify({
        "success": True,
        "username": username,
        "balance": balance
    })