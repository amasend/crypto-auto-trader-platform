import psycopg2 as psycopg2
from passlib.hash import sha256_crypt


class DatabaseClient:

    def __init__(self, dbname: str, username: str, password: str, host: str):
        connection = psycopg2.connect(f"host={host} dbname={dbname} user={username} password={password}")
        self.connection = connection
        self.cursor = self.connection.cursor()


def create_user(connection, cursor, username, password, api_key):
    """ Inserts username, password and an api key to the database """
    try:
        cursor.execute("""INSERT INTO users (username,password, api_key)
        VALUES(%s, %s, %s)
        returning user;""", (username, password, api_key))
        connection.commit()
        return "User created"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def hash_password(password):
    """ This function hashes password """
    hashed_password = sha256_crypt.hash(password)
    return hashed_password
