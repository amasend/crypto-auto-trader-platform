import unittest
from api.database.database_manager import create_user, DatabaseClient
import requests


class MyTestCase(unittest.TestCase):
    def test_is_user_created(self):
        client = DatabaseClient("users", "admin", "zaq1@WSX", "localhost")
        create_user_res = requests.post("http://localhost:5000/users",
                                        headers={"content-type": "text", "username": "test", "password": "test"})
        result = create_user_res.headers["result"]
        self.assertEqual(result, "User created", "Create user request should return 'User created'")


if __name__ == '__main__':
    unittest.main()
