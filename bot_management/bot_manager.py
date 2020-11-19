import uuid
from bot_management.bot_body import Bot
import threading
my_array = []


class BotManager:
    """This Class contains functions used by user to create bot"""

    def create_bot_id(self):
        """Returns id, that can be used in creating new bot"""
        return str(uuid.uuid4())

    def run_bot(self, bot_id: int, api_key: int, api_secret: int, symbol: str):
        """starts bot in new thread when given
            id returned to user by create_bot_id: bot_id
            not private key of the user: api_ key
            private key of the user: api_secret
            test variable is only used in tests and isn't necessary"""
        my_bot = Bot(bot_id)
        my_array.append(my_bot)
        thread = threading.Thread(target=my_bot.start_bot, args=[api_key, api_secret, symbol])
        thread.start()

    def stop_bot(self, bot_id: int):
        """if given id of the bot that is running, this function will stop it"""
        for x in range(0, len(my_array)):
            if my_array[x].bot_id == bot_id:
                my_array[x].running = False


