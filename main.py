import threading
from TS3Bot import TS3Bot

from modules.move_afk import move_afk
from modules.holiday_doodle import set_holiday_doodle


def main():
    bot = TS3Bot()

    holiday_doodle_thread = threading.Thread(target=set_holiday_doodle, kwargs={'bot': bot})
    move_afk_thread = threading.Thread(target=move_afk, kwargs={'bot': bot})

    holiday_doodle_thread.start()
    move_afk_thread.start()

    move_afk_thread.join()

    bot.exit()


if __name__ == '__main__':
    main()
