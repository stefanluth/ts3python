import datetime

from TS3Bot import TS3Bot
from configuration import BANNERS


def set_holiday_doodle(bot: TS3Bot):
    today = datetime.datetime.today()
    if today.month == 2 and 12 <= today.day <= 14:
        return bot.change_host_banner_image(BANNERS['valentines'])
    elif today.month == 4 and today.day == 1:
        return bot.change_host_banner_image(BANNERS['april fools'])
    elif today.month == 5 and 7 <= today.day <= 15 and today.weekday() == 6:
        return bot.change_host_banner_image(BANNERS['mothers day'])
    elif today.month == 10 and 24 <= today.day <= 31:
        return bot.change_host_banner_image(BANNERS['halloween'])
    elif today.month == 12 and 1 <= today.day <= 26:
        return bot.change_host_banner_image(BANNERS['christmas'])
    elif (today.month == 12 and 27 <= today.day) or (today.month == 1 and 1 <= today.day <= 5):
        return bot.change_host_banner_image(BANNERS['new years'])
    elif today.year == 2022 and today.month == 4 and 14 <= today.day <= 18:
        return bot.change_host_banner_image(BANNERS['easter'])
    elif today.year == 2022 and today.month == 5 and today.day == 26:
        return bot.change_host_banner_image(BANNERS['fathers day'])
    elif today.year == 2023 and today.month == 4 and 6 <= today.day <= 10:
        return bot.change_host_banner_image(BANNERS['easter'])
    elif today.year == 2023 and today.month == 5 and today.day == 18:
        return bot.change_host_banner_image(BANNERS['fathers day'])
    elif today.year == 2024 and today.month == 3 and 28 <= today.day <= 31:
        return bot.change_host_banner_image(BANNERS['easter'])
    elif today.year == 2024 and today.month == 5 and today.day == 9:
        return bot.change_host_banner_image(BANNERS['fathers day'])
    else:
        return bot.change_host_banner_image(BANNERS['default'])
