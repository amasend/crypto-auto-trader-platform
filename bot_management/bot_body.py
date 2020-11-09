from time import sleep, ctime
import helpfull_functions
from history_writer.history_writer import upload_data


class Bot:
    def __init__(self, bot_id:str, time_to_live):
        self.bot_id = bot_id
        self.time_to_live = time_to_live

    def switcher(self, i="waiting"):
        client = helpfull_functions.setup_client("localhost", "8086", "test_bot_logs")
        json_body = [
            {
                "measurement": "bot_action",
                "tag": {self.bot_id},
                "time": ctime(),
                "fields": {
                    "time to live": self.time_to_live,
                    "action": i
                }
            }]

        if i == "invest":
            upload_data(client)
            client.write_points(json_body)
            print(f"{self.bot_id} investing function")

        elif i == "sell":
            client.write_points(json_body)
            print(f"{self.bot_id} selling function")

        else:
            client.write_points(json_body)
            print(f"{self.bot_id} waiting")

    def start_bot(self):
        """bot function that does all what bot does"""
        while self.time_to_live > 0:
            Bot.switcher(self)
            self.time_to_live = self.time_to_live - 1
            print(self.time_to_live)
            sleep(60)

#on the spot starting bot for testing
# Bot(11, 3).start_bot()
#on the spot testing if influxdb got the logs about what bot have done
# print(helpfull_functions.reading_influxdb_query(
#     client=helpfull_functions.setup_client("localhost", "8086", "test_bot_logs"),
#     name_of_database="bot_action"))
