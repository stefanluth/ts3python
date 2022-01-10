import datetime
import time

from configuration import TRACK_TOGGLE_CMD, DO_NOT_TRACK_CONFIRMED_MSG, TRACKING_INFO_MSG
from SQLiteDB import SQLiteDB
from TS3Bot import TS3Bot


def start_time_measurement(bot: TS3Bot, database: SQLiteDB, interval: int):
    messaged_clients = list()
    first_timecheck = round(datetime.datetime.now().timestamp(), 3)
    while 1:
        clients_b64 = list()
        clients = bot.create_client_list()
        for client in clients:
            database.create_profile(client)
            clients_b64.append(client.b64_uid)

            if client.b64_uid in messaged_clients:
                continue

            if database.get_do_not_track(client):
                bot.send_private_message(client_id=client.id, msg=DO_NOT_TRACK_CONFIRMED_MSG)
            else:
                bot.send_private_message(client_id=client.id, msg=TRACKING_INFO_MSG)

            messaged_clients.append(client.b64_uid)

        for message in bot.unused_messages:
            if message.content == TRACK_TOGGLE_CMD:
                message.mark_as_used()
                for client in clients:
                    if client.id != message.invoker_id:
                        continue

                    toggled_on = database.toggle_do_not_track(client)

                    if toggled_on:
                        bot.send_private_message(client_id=client.id, msg=DO_NOT_TRACK_CONFIRMED_MSG)
                    else:
                        bot.send_private_message(client_id=client.id, msg=TRACKING_INFO_MSG)
                    break

        time.sleep(interval)

        second_timecheck = round(datetime.datetime.now().timestamp(), 3)
        time_difference = round(second_timecheck - first_timecheck, 2)
        first_timecheck = second_timecheck

        for client in bot.create_client_list():
            if client.b64_uid not in clients_b64:
                continue

            client_profile = database.get_profile(client)
            do_not_track = client_profile['do_not_track']

            if do_not_track:
                continue

            client_total = client_profile['connected_total']
            new_total = round(client_total + time_difference, 2)
            database.update_profile_total(client, new_total)

            if client.in_afk_channel:
                client_afk = client_profile['connected_afk']
                new_afk = round(client_afk + time_difference, 2)
                database.update_profile_afk(client, new_afk)
