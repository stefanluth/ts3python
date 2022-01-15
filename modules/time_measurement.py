import datetime
import time

from configuration import TRACK_TOGGLE_CMD, TRACKING_INFO_MSG, DO_NOT_TRACK_CONFIRMED_MSG, \
    MEASUREMENT_EMPTY_INTERVAL_SECONDS, MEASUREMENT_INTERVAL_SECONDS

from ProfilesDB import ProfilesDB
from TS3Bot import TS3Bot


def start_time_measurement(bot: TS3Bot, database: ProfilesDB):
    messaged_clients = list()
    first_timecheck = round(datetime.datetime.now().timestamp(), 3)
    while 1:
        clients = bot.create_client_list()

        if len(clients) == 0:
            messaged_clients = list()
            time.sleep(MEASUREMENT_EMPTY_INTERVAL_SECONDS)
            continue

        clients_b64 = list()

        for client in clients:
            database.create_profile(client)
            clients_b64.append(client.b64_uid)

            if client.b64_uid in messaged_clients:
                continue

            do_not_track = database.get_do_not_track(client)
            inform_client(bot, client, do_not_track)
            messaged_clients.append(client.b64_uid)

        check_messages(bot, clients, database)

        time.sleep(MEASUREMENT_INTERVAL_SECONDS)

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

            if not client.in_afk_channel:
                continue

            client_afk = client_profile['connected_afk']
            new_afk = round(client_afk + time_difference, 2)
            database.update_profile_afk(client, new_afk)


def check_messages(bot, clients, database):
    for message in bot.unused_messages:
        if message.content != TRACK_TOGGLE_CMD:
            continue

        message.mark_as_used()

        for client in clients:
            if client.id != message.invoker_id:
                continue

            do_not_track = database.toggle_do_not_track(client)
            inform_client(bot, client, do_not_track)

            break


def inform_client(bot, client, do_not_track):
    if do_not_track:
        msg = DO_NOT_TRACK_CONFIRMED_MSG
    else:
        msg = TRACKING_INFO_MSG

    bot.send_private_message(client_id=client.id, msg=msg)
