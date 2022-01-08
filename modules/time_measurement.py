import datetime
import time

from SQLiteDB import SQLiteDB
from TS3Bot import TS3Bot


def start_time_measurement(bot: TS3Bot, database: SQLiteDB, interval: int):
    first_timecheck = round(datetime.datetime.now().timestamp(), 3)
    while 1:
        clients_b64 = list()
        for client in bot.create_client_list():
            database.create_profile(client)
            clients_b64.append(client.b64_uid)

        time.sleep(interval)

        second_timecheck = round(datetime.datetime.now().timestamp(), 3)
        time_difference = round(second_timecheck-first_timecheck, 2)
        first_timecheck = second_timecheck

        for client in bot.create_client_list():
            if client.b64_uid in clients_b64:
                if client.in_afk_channel:
                    client_afk = database.get_profile_afk(client)
                    new_afk = round(client_afk+time_difference, 2)
                    database.update_profile_afk(client, new_afk)
                client_total = database.get_profile_total(client)
                new_total = round(client_total+time_difference, 2)
                database.update_profile_total(client, new_total)
