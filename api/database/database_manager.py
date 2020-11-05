import psycopg2 as psycopg2
from passlib.hash import sha256_crypt


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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "Error"


def add_exchange(connection, cursor, username, password, exchange_name, exchange_api_key):
    """ This function adds users' exchange
        Paramaters
        ------------
        connection: connection required - postresql connection
        cursor: connection required - postresql connection
        username: str required - username
        password: str required - password
        exchange_name: str required - name of and exchange, e.g. binance
        exchange_api_key: str required - api key from an exchange, e.g. from binance
    """
    try:
        cursor.execute("""SELECT * FROM users
        WHERE username = '{0}'""".format(username))
        user_data = cursor.fetchall()[0]
        username = user_data[0]
        db_password = user_data[1]  # hashed password from database
        user_api_key = user_data[2]
        if username == username and sha256_crypt.verify(password, db_password):
            # VERIFIED - username and password are correct

            cursor.execute("""INSERT INTO exchanges
            VALUES('{0}', '{1}', '{2}', '{3}');""".format(exchange_name, username, exchange_api_key, user_api_key))
            connection.commit()
            return "Exchange created"
        else:
            # NOT VERIFIED - username or password is incorrect
            return "Username or password is incorrect"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "Error"


def hash_password(password):
    """ This function hashes password """
    hashed_password = sha256_crypt.hash(password)
    return hashed_password
