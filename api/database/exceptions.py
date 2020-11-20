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


class UserExistsException(Exception):
    def __init__(self):
        self.message = "User already exists"

    def __str__(self):
        return self.message


class CurrentPricesException(Exception):
    def __init__(self):
        self.message = "Wrong cryptocurrency symbol or exchange name"

    def __str__(self):
        return self.message
