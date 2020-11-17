class AuthenticationException(Exception):
    def __init__(self):
        self.message = "Username or password is incorrect"

    def __str__(self):
        return self.message


class DatabaseException(Exception):
    def __init__(self):
        self.message = "Something went wrong with database... try again"

    def __str__(self):
        return self.message
