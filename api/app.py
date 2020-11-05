from flask import *
from api.database.database_manager import DatabaseClient, create_user, hash_password
import secrets

app = Flask(__name__)

client = DatabaseClient('users', "admin", "zaq1@WSX", "localhost")


# user creates an account
@app.route("/users", methods=["POST"])
def create_account():
    """ This function receives username and password and passes it to the database
        it also generates api key """
    username = request.headers['username']
    password = request.headers['password']
    hashed_password = hash_password(password)
    api_key = secrets.token_urlsafe(30)
    response = make_response()
    create_user(client.connection, client.cursor, username, hashed_password, api_key)
    return response, 200


# user creates a bot
@app.route("/bots", methods=["POST"])
def create_bot():
    return "Bot created", 200


# user gets a current price
@app.route("/current-prices", methods=["GET"])
def current_prices():
    return "Current prices", 200


# user gets his trade history
@app.route("/trade-history", methods=["GET"])
def trade_history_():
    return "Trade history", 200


# NOTE: all returns are mocked for now

if __name__ == "__main__":
    app.run(debug=True)
