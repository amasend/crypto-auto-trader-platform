from flask import Flask

app = Flask(__name__)

# user creates account
@app.route("/users", methods=["POST"])
def create_account(username,password):
    return f"Hello f{username}"

# user creates a bot
@app.route("/<apiKey>/bots",methods=["POST"])
def create_bot():
    return "Bot created"

# user gets a current price
@app.route("/current-prices",methods=["GET"])
def current_prices():
    return "Current prices"

# user gets his trade history
@app.route("/<apiKey>/trade-history",methods=["GET"])
def trade_history_():
    return "Trade history"

# NOTE: all returns are mocked for now

if __name__ == "__main__":
    app.run(debug=True)
