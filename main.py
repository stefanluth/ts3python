import threading

from configuration import BOT_NAME
from modules.move_afk import move_afk
from modules.holiday_doodle import set_holiday_doodle
from modules.time_measurement import start_time_measurement

from Database import Database
from TS3Bot import TS3Bot


def main():
    database = Database()
    bot = TS3Bot()
    bot.set_bot_name(BOT_NAME)

    holiday_doodle_thread = threading.Thread(target=set_holiday_doodle, kwargs={'bot': bot})
    move_afk_thread = threading.Thread(target=move_afk, kwargs={'bot': bot})
    time_measurement_thread = threading.Thread(target=start_time_measurement, kwargs={'bot': bot,
                                                                                      'database': database})

    holiday_doodle_thread.start()
    move_afk_thread.start()
    time_measurement_thread.start()

    holiday_doodle_thread.join()
    move_afk_thread.join()
    time_measurement_thread.join()

    bot.exit()


if __name__ == '__main__':
    main()
