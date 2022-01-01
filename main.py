from TS3Bot import TS3Bot


def main():
    bot = TS3Bot()

    bot.send_channel_message('Hello channel!')

    bot.exit()


if __name__ == '__main__':
    main()
