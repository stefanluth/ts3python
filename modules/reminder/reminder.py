import calendar
import datetime

from ts3bot import TS3Bot
from .configuration import REMINDER_3_DAYS_MSG, REMINDER_TODAY_MSG

days = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}


def crackerbarrel_reminder(bot: TS3Bot):
    today = datetime.datetime.today()
    wednesday = days['Wednesday']
    last_wednesday = last_weekday_of_month(wednesday, today.year, today.month)

    if today.day == last_wednesday:
        bot.set_host_message_mode(2)
        return bot.set_new_host_message(REMINDER_TODAY_MSG)
    elif today.day == last_wednesday - 3:
        bot.set_host_message_mode(2)
        return bot.set_new_host_message(REMINDER_3_DAYS_MSG)
    elif today.day == last_wednesday + 1:
        return bot.reset_host_message()


def last_weekday_of_month(day: int, year: int, month: int):
    current_month = calendar.monthcalendar(year, month)
    for week in reversed(current_month):
        if week[day]:
            return week[day]
