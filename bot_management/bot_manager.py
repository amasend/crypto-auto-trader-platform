import uuid
from bot_management.bot_body import Bot
import threading
from bot_management.my_keys import *

my_array = []
class BotManager:
    """This Class contains functions used by user to create bot"""

    def create_bot_id(self):
        """After signal to create a bot user will get get id that will be used in his creation"""
        return str(uuid.uuid4())

    def run_bot(self, bot_id, api_key, api_secret, test=0):
        """starts bot in new thread"""
        my_bot = Bot(bot_id)
        my_array.append(my_bot)
        thread = threading.Thread(target=my_bot.start_bot, args=[api_key, api_secret, test])
        thread.start()

    def stop_bot(self, bot_id):
        """stops bot with specified id"""
        for x in range(0, len(my_array)):
            if my_array[x].bot_id == bot_id:
                my_array[x].running = False

# fast example of usage
# api_key = api_test_key()
# api_secret = api_test_secret_key()
# BotManager().run_bot(123456789, api_key, api_secret)
# BotManager().stop_bot(123456789)

