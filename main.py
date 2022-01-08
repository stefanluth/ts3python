import threading

from credentials import SERVER_IP, SERVER_PORT, TELNET_LOGIN, TELNET_PW, TELNET_PORT
from configuration import BOT_NAME, DATABASE_NAME
from modules.crackerbarrel_reminder import crackerbarrel_reminder
from modules.holiday_doodle import set_holiday_doodle
from modules.move_afk import move_afk
from modules.time_measurement import start_time_measurement

from Database import Database
from TS3Bot import TS3Bot


def main():
    database = Database(name=DATABASE_NAME)
    bot = TS3Bot(ip=SERVER_IP,
                 port=SERVER_PORT,
                 login=TELNET_LOGIN,
                 password=TELNET_PW,
                 telnet_port=TELNET_PORT)

    bot.set_bot_name(BOT_NAME)

    crackerbarrel_reminder_thread = threading.Thread(target=crackerbarrel_reminder, kwargs={'bot': bot})
    holiday_doodle_thread = threading.Thread(target=set_holiday_doodle, kwargs={'bot': bot})
    move_afk_thread = threading.Thread(target=move_afk, kwargs={'bot': bot})
    time_measurement_thread = threading.Thread(target=start_time_measurement, kwargs={'bot': bot,
                                                                                      'database': database})

    crackerbarrel_reminder_thread.start()
    holiday_doodle_thread.start()
    move_afk_thread.start()
    time_measurement_thread.start()

    crackerbarrel_reminder_thread.join()
    holiday_doodle_thread.join()
    move_afk_thread.join()
    time_measurement_thread.join()

    bot.exit()


if __name__ == '__main__':
    main()
