from flask import Flask
from db import connect_db, create_db, add_player, player_exists, get_player, update_balance

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Witamy w Emerald Casino!</p>"

if __name__ == "__main__":
    app.run(debug=True)