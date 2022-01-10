# Bot
BOT_NAME = 'Bot'
BOT_DESC = ''
BOT_AVAT = ''

# Channels
AFK_CHANNELS = [345, 567, 678, 789]
BUSY_CHANNEL = 345  # Busy

# Module specifics
WORDPRESS_UPDATE_INTERVAL_SECONDS = 15 * 60
IDLE_MINUTES_BEFORE_MOVE = 20
CHECK_AFK_INTERVAL_SECONDS = 10
MEASUREMENT_INTERVAL_SECONDS = 5
AFK_MOVED_MESSAGE = 'You were moved because of inactivity.'

DO_NOT_TRACK_TOGGLE_COMMAND = '!toggle'
DO_NOT_TRACK_CONFIRMED_MSG = f'Your connection time is not being tracked anymore. ' \
                             f'{DO_NOT_TRACK_TOGGLE_COMMAND} to undo.'
TRACKING_INFO_MSG = f'Your connection time is being tracked. To refuse tracking, enter {DO_NOT_TRACK_TOGGLE_COMMAND}.'

CRACKERBARREL_REMINDER_3_DAYS = 'Crackerbarrel meeting in 3 days!'
CRACKERBARREL_REMINDER_TODAY = 'Crackerbarrel meeting today 8pm!'

BANNERS = {
    'default': 'https://your-domain.com/files/banner-default.png',
    'covid': 'https://your-domain.com/files/banner-corona.png',
    'valentines': 'https://your-domain.com/files/banner-valentines.png',
    'eastern': 'https://your-domain.com/files/banner-eastern.png',
    'april fools': 'https://your-domain.com/files/banner-april-fools.png',
    'mothers day': 'https://your-domain.com/files/banner-mothers-day.png',
    'fathers day': 'https://your-domain.com/files/banner-fathers-day.png',
    'halloween': 'https://your-domain.com/files/banner-halloween.png',
    'christmas': 'https://your-domain.com/files/banner-christmas.png',
    'new years': 'https://your-domain.com/files/banner-new-year.png',
           }
