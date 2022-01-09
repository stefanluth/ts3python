import threading
import time

from credentials import *
from configuration import BOT_NAME, PROFILES_DB_NAME, MEASUREMENT_INTERVAL_SECONDS
from modules.time_measurement import start_time_measurement

from SQLiteDB import SQLiteDB
from TS3Bot import TS3Bot


def main():
    bot = TS3Bot(ip=SERVER_IP,
                 port=SERVER_PORT,
                 login=TELNET_LOGIN,
                 password=TELNET_PW,
                 telnet_port=TELNET_PORT)

    bot.set_bot_name(BOT_NAME)

    bot.enable_receive_all_messages()

    profile_db = SQLiteDB(PROFILES_DB_NAME)

    time_measurement_thread = threading.Thread(target=start_time_measurement,
                                               kwargs={
                                                   'bot': bot,
                                                   'database': profile_db,
                                                   'interval': MEASUREMENT_INTERVAL_SECONDS,
                                               })

    # time_measurement_thread.start()
    # time_measurement_thread.join()

    print(bot.get_client_list())

    time.sleep(5)

    bot.whoami()

    for message in bot.messages:
        print(message.raw)
        if message.type == 'private':
            bot.send_private_message(message.invoker_id, f'hallo {message.invoker_name}')
        elif message.type == 'channel':
            bot.send_channel_message('hallo channel')

    time.sleep(5)

    bot.exit()


if __name__ == '__main__':
    main()
