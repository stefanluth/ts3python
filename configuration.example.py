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
MEASUREMENT_EMPTY_INTERVAL_SECONDS = 5 * 60

AFK_MOVED_MESSAGE = 'You were moved because of inactivity.'

TRACK_TOGGLE_CMD = '!toggle'
TRACKING_INFO_MSG = f'Your connection time is being tracked. To opt-out, enter [b]{TRACK_TOGGLE_CMD}[/b].'
DO_NOT_TRACK_CONFIRMED_MSG = f'Your connection time is not being tracked anymore. ' \
                             f'[b]{TRACK_TOGGLE_CMD}[/b] to undo.'

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


# Games specifics
ACCOUNTS_DB_NAME = 'accounts'
ACCOUNT_START_BALANCE = 5000
ACCOUNT_INFO_BALANCE = 'Your balance is {}.'

GAME_INVALID_CMD = 'Please enter a valid command.'
GAME_INVALID_AMOUNT = 'Please enter a valid amount.'
GAME_INVALID_GAME = 'Please enter a valid game.'
GAME_ABORT_BAD_BET = 'Please enter a valid bet!'
GAME_ABORT_BROKE = 'Sorry, you don\'t have enough money!'
GAME_ABORT_BAD_WAGER = 'Sorry, minimum wager is {}!'
GAME_GREETINGS = 'Hello {}. Thank you for playing!'  # player_name
GAME_WON_MSG = 'You win [b][color={0}]{1}[/color][/b]!!'  # color, win_amount
GAME_LOST_MSG = 'Oh no! You lost [b][color=firebrick]{}[/color][/b]!'  # wager

# Slots
SLOTS_MIN_WAGER = 50
SLOTS_START_MSG = 'You started the slot machine! Good luck!'
SLOTS_RESULT_MSG = 'Your reels show:'

# Roulette
ROULETTE_MIN_WAGER = 50
ROULETTE_START_MSG = 'You bet [b]{0}[/b] on {1}! Let\'s spin the wheel!'  # amount, number or name
ROULETTE_RESULT_MSG = 'The ball lands on [b]{}[/b]!!'  # winning_number
