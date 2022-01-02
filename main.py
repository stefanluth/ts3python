from TS3Bot import TS3Bot
from configuration import BOT_NAME


def main():
    bot = TS3Bot()
    bot.set_bot_name(BOT_NAME)
    bot.send_channel_message('Hello channel!')
    bot.exit()


if __name__ == '__main__':
    main()
