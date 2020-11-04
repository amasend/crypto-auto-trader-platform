import unittest
from api.database.database_manager import create_user, DatabaseClient


class MyTestCase(unittest.TestCase):
    def test_is_user_created(self):
        client = DatabaseClient("users", "admin", "zaq1@WSX", "localhost")
        create_user_result = create_user(client.connection, client.cursor, "test", "test", "test")
        client.cursor.close()
        self.assertEqual(create_user_result, "User created", "create_user method should return message 'User created'")


if __name__ == '__main__':
    unittest.main()
