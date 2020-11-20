import psycopg2 as psycopg2
from passlib.hash import sha256_crypt
import ccxt
from api.database.exceptions import AuthenticationException, DatabaseException
from time import ctime

class DatabaseClient:
    """ Paramaters
        ------------
        dbname: str required - name of the database
        username: str required - database username
        password: str required - database password
        host: str required - name of your host , e.g. localhost
    """

    def __init__(self, dbname: str, username: str, password: str, host: str):
        connection = psycopg2.connect(f"host={host} dbname={dbname} user={username} password={password}")
        self.connection = connection
        self.cursor = self.connection.cursor()


def create_user(connection, cursor, username, password, api_key):
    """ Inserts username, password and an api key to the database
    """
    try:
        cursor.execute("""INSERT INTO users (username,password, api_key)
        VALUES(%s, %s, %s)
        returning user;""", (username, password, api_key))
        connection.commit()
        return "User created"
    except:
        return UserExistsException().message


# NOTE: This function will be implemented soon, I know that the code is doubled below

def authenticate_user(cursor, username, password):
    try:
        cursor.execute("""SELECT * FROM users
                WHERE username = '{0}'""".format(username))
        user_data = cursor.fetchall()[0]
        username = user_data[0]
        db_password = user_data[1]  # hashed password from database
        if username == username and sha256_crypt.verify(password, db_password):
            # VERIFIED - username and password are correct
            return user_data
        else:
            return AuthenticationException().message
    except:
        # NOT VERIFIED - username or password is incorrect
        return AuthenticationException().message


def add_exchange(connection, cursor, username, password, exchange_name, exchange_api_key, secret):
    """ This function adds users' exchange
        Paramaters
        ------------
        connection: connection required - postresql connection
        cursor: connection required - postresql connection
        username: str required - username
        password: str required - password
        exchange_name: str required - name of and exchange, e.g. binance
        exchange_api_key: str required - api key from an exchange, e.g. from binance
        secret: str required - secret api key from an exchange, e.g. from binance
    """
    user_data = authenticate_user(cursor, username, password)
    if user_data != False:
        try:
            user_api_key = user_data[2]
            cursor.execute("""INSERT INTO exchanges
            VALUES('{0}', '{1}', '{2}', '{3}', '{4}');""".format(exchange_name, username, exchange_api_key,
                                                                 user_api_key, secret))
            connection.commit()
            return "Exchange addded to account"
        except:
            return DatabaseException().message
    else:
        return AuthenticationException().message


def hash_password(password):
    """ This function hashes password """
    hashed_password = sha256_crypt.hash(password)
    return hashed_password


def get_user_trades(cursor, username, password, exchange_name, symbol):
    """ Getting user trades
        Paramaters
        ------------
        cursor: connection required - postresql connection
        username: str required - username
        password: str required - password
        exchange_name: str required - name of and exchange, e.g. binance
        symbol: str - symbol of cryptocurrency, e.g. BTC/USDT
    """
    user_data = authenticate_user(cursor, username, password)

    if not user_data:
        try:
            user_api_key = user_data[2]
            cursor.execute("""SELECT * FROM exchanges
                        WHERE user_api_key = '{0}'""".format(user_api_key))
            exchange_data = cursor.fetchall()[0]
            exchange_api_key = exchange_data[2]
            secret = exchange_data[4]

            exchange = getattr(ccxt, exchange_name)({'options': {'adjustForTimeDifference': True}})
            exchange.apiKey = exchange_api_key
            exchange.secret = secret
            if exchange.has['fetchMyTrades']:
                return exchange.fetch_my_trades(symbol=symbol)
        except:
            return DatabaseException().message
    else:
        return AuthenticationException().message


def log_current_state_of_the_bot(client: object, bot_id: int, action: str):
    """Used to save to table bot_runtime_logs current state of the bot with specified id
        in order for it to work, table named bot_runtime_logs should be created beforehand
        client: object - postgresql client logged beforehand
        bot_id: int - id of bot that is changing state
        action: str - CREATED/STARTED/STOPPED according to the action taken by bot)"""
    postgres_insert_query = """ INSERT INTO bot_runtime_logs (ID, ACTION, TIMESTAMP) VALUES (%s,%s,%s)"""
    record_to_insert = (bot_id, f'{action}', ctime())
    client.cursor.execute(postgres_insert_query, record_to_insert)
    client.connection.commit()
