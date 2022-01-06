import calendar
import datetime

from TS3Bot import TS3Bot
from configuration import CRACKERBARREL_REMINDER_3_DAYS, CRACKERBARREL_REMINDER_TODAY


def crackerbarrel_reminder(bot: TS3Bot):
    today = datetime.datetime.today()
    last_wednesday = _get_last_wednesday(today.year, today.month)

    if today.day == last_wednesday:
        bot.set_host_message_mode(2)
        return bot.set_new_host_message(CRACKERBARREL_REMINDER_TODAY)
    elif today.day == last_wednesday - 3:
        bot.set_host_message_mode(2)
        return bot.set_new_host_message(CRACKERBARREL_REMINDER_3_DAYS)
    elif today.day == last_wednesday + 1:
        return bot.reset_host_message()


def _get_last_wednesday(year: int, month: int):
    current_month = calendar.monthcalendar(year, month)
    for week in reversed(current_month):
        if week[2]:
            return week[2]
