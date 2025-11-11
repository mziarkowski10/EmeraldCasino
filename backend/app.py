from flask import Flask
from routes import routes
from db import create_db

app = Flask(__name__)

create_db()

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)