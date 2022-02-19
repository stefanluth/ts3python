import threading

from configuration import BOT_NAME, BOT_DESC
from credentials import *

from modules.reminder import reminder
from modules.doodle import doodle
from modules.afk_mover import afk_mover

from modules.games import games, AccountDB
from modules.games.configuration import ACCOUNTS_DB_NAME

from modules.time_tracker import time_tracker, wordpress, ProfilesDB, WordpressDB
from modules.time_tracker.configuration import PROFILES_DB_NAME

from ts3bot import TS3Bot


def main():
    bot = TS3Bot(ip=SERVER_IP,
                 port=SERVER_PORT,
                 login=TELNET_LOGIN,
                 password=TELNET_PW,
                 telnet_port=TELNET_PORT)

    bot.set_bot_name(BOT_NAME)
    bot.set_bot_description(BOT_DESC)
    bot.enable_receive_all_messages()

    accounts_db = AccountDB(ACCOUNTS_DB_NAME)
    profile_db = ProfilesDB(PROFILES_DB_NAME)
    wordpress_db = WordpressDB(MYSQL_HOST, MYSQL_DB_NAME, MYSQL_USER, MYSQL_PW, 'stats')

    crackerbarrel_reminder_thread = threading.Thread(target=reminder.check_crackerbarrel_reminder, kwargs={'bot': bot})
    holiday_doodle_thread = threading.Thread(target=doodle.set_holiday_doodle, kwargs={'bot': bot})
    move_afk_thread = threading.Thread(target=afk_mover.move_afk, kwargs={'bot': bot})

    games_thread = threading.Thread(target=games.start,
                                    kwargs={
                                        'bot': bot,
                                        'database': accounts_db,
                                    })

    time_measurement_thread = threading.Thread(target=time_tracker.start_tracker,
                                               kwargs={
                                                   'bot': bot,
                                                   'database': profile_db,
                                               })

    wordpress_update_thread = threading.Thread(target=wordpress.update_post,
                                               kwargs={
                                                   'profile_db': profile_db,
                                                   'wordpress_db': wordpress_db,
                                               })

    crackerbarrel_reminder_thread.start()
    games_thread.start()
    holiday_doodle_thread.start()
    move_afk_thread.start()
    time_measurement_thread.start()
    wordpress_update_thread.start()

    crackerbarrel_reminder_thread.join()
    games_thread.join()
    holiday_doodle_thread.join()
    move_afk_thread.join()
    time_measurement_thread.join()
    wordpress_update_thread.join()

    bot.exit()


if __name__ == '__main__':
    main()
