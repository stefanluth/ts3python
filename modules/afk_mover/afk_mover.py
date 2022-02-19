import time
from ts3bot import TS3Bot
from .configuration import BUSY_CHANNEL, CHECK_AFK_INTERVAL_SECONDS, AFK_MOVED_MESSAGE


def move_afk(bot: TS3Bot):
    while 1:
        for client in bot.create_client_list():
            if client.is_afk and not client.in_afk_channel:
                bot.move_client(client.id, BUSY_CHANNEL)
                bot.send_private_message(client.id, AFK_MOVED_MESSAGE)
        time.sleep(CHECK_AFK_INTERVAL_SECONDS)
