from flask import *
from api.database.database_manager import DatabaseClient, create_user, hash_password, add_exchange
import secrets
from downloader.current_data_provider.provider_manager import download_current_data

app = Flask(__name__)

client = DatabaseClient("crypto-trader", "admin", "zaq1@WSX", "localhost")


# user creates an account
@app.route("/users", methods=["POST"])
def create_account():
    """ This function receives username and password and passes it to the database
        it also generates api key """
    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_password(password)
    api_key = secrets.token_urlsafe(30)
    create_user_result = create_user(client.connection, client.cursor, username, hashed_password, api_key)
    response = make_response()
    response.headers["result"] = create_user_result
    return response, 200


# user adds an exchange
@app.route("/exchanges", methods=["POST"])
def create_exchange():
    username = request.form['username']
    password = request.form['password']
    exchange_name = request.form['exchange_name']
    exchange_api_key = request.form['exchange_api_key']
    add_exchange_result = add_exchange(client.connection, client.cursor, username, password, exchange_name, exchange_api_key)
    return add_exchange_result, 200


# user creates a bot
@app.route("/bots", methods=["POST"])
def create_bot():
    return "Bot created", 200


# user gets a current price
@app.route("/current-prices", methods=["GET"])
def current_prices():
    params = request.args
    crypto_symbol = params.getlist('symbol')[0]
    exchange_name = params.getlist('exchange')[0]
    crypto_symbol = crypto_symbol.replace("_", "/")
    crypto_current_data = download_current_data(exchange_name, crypto_symbol)
    return crypto_current_data, 200


# user gets his trade history
@app.route("/trade-history", methods=["GET"])
def trade_history_():
    return "Trade history"


# NOTE: all returns are mocked for now

if __name__ == "__main__":
    app.run(debug=True)
