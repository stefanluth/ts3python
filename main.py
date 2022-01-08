import threading

from credentials import *
from configuration import BOT_NAME, PROFILES_DB_NAME
from modules.update_wordpress import update_wordpress

from Database import Database
from WordpressDB import WordpressDB
from TS3Bot import TS3Bot


def main():
    bot = TS3Bot(ip=SERVER_IP,
                 port=SERVER_PORT,
                 login=TELNET_LOGIN,
                 password=TELNET_PW,
                 telnet_port=TELNET_PORT)

    bot.set_bot_name(BOT_NAME)

    profile_db = Database(PROFILES_DB_NAME)
    wordpress_db = WordpressDB(MYSQL_HOST, MYSQL_DB_NAME, MYSQL_USER, MYSQL_PW, 'stats')

    wordpress_update_thread = threading.Thread(target=update_wordpress, kwargs={'profile_db': profile_db,
                                                                                'wordpress_db': wordpress_db})

    wordpress_update_thread.start()
    wordpress_update_thread.join()

    bot.exit()


if __name__ == '__main__':
    main()
