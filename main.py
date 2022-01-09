import threading

from credentials import *
from configuration import BOT_NAME, PROFILES_DB_NAME, MEASUREMENT_INTERVAL_SECONDS, WORDPRESS_UPDATE_INTERVAL_SECONDS
from modules.crackerbarrel_reminder import crackerbarrel_reminder
from modules.holiday_doodle import set_holiday_doodle
from modules.move_afk import move_afk
from modules.time_measurement import start_time_measurement
from modules.update_wordpress import update_wordpress

from SQLiteDB import SQLiteDB
from TS3Bot import TS3Bot
from WordpressDB import WordpressDB


def main():
    bot = TS3Bot(ip=SERVER_IP,
                 port=SERVER_PORT,
                 login=TELNET_LOGIN,
                 password=TELNET_PW,
                 telnet_port=TELNET_PORT)

    bot.set_bot_name(BOT_NAME)
    bot.enable_receive_all_messages()

    profile_db = SQLiteDB(PROFILES_DB_NAME)
    wordpress_db = WordpressDB(MYSQL_HOST, MYSQL_DB_NAME, MYSQL_USER, MYSQL_PW, 'stats')

    crackerbarrel_reminder_thread = threading.Thread(target=crackerbarrel_reminder, kwargs={'bot': bot})
    holiday_doodle_thread = threading.Thread(target=set_holiday_doodle, kwargs={'bot': bot})
    move_afk_thread = threading.Thread(target=move_afk, kwargs={'bot': bot})
    time_measurement_thread = threading.Thread(target=start_time_measurement,
                                               kwargs={
                                                   'bot': bot,
                                                   'database': profile_db,
                                                   'interval': MEASUREMENT_INTERVAL_SECONDS,
                                               })
    wordpress_update_thread = threading.Thread(target=update_wordpress,
                                               kwargs={
                                                   'profile_db': profile_db,
                                                   'wordpress_db': wordpress_db,
                                                   'interval': WORDPRESS_UPDATE_INTERVAL_SECONDS,
                                               })

    crackerbarrel_reminder_thread.start()
    holiday_doodle_thread.start()
    move_afk_thread.start()
    time_measurement_thread.start()
    wordpress_update_thread.start()

    crackerbarrel_reminder_thread.join()
    holiday_doodle_thread.join()
    move_afk_thread.join()
    time_measurement_thread.join()
    wordpress_update_thread.join()

    bot.exit()


if __name__ == '__main__':
    main()
