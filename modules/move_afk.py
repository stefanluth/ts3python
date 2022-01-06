import time
from TS3Bot import TS3Bot
from configuration import BUSY_CHANNEL, CHECK_AFK_INTERVAL_SECONDS


def move_afk(bot: TS3Bot):
    while 1:
        for client in bot.create_client_list():
            if client.is_afk and not client.in_afk_channel:
                bot.move_client(client.id, BUSY_CHANNEL)
        time.sleep(CHECK_AFK_INTERVAL_SECONDS)
