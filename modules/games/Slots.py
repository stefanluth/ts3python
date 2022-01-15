import random
import time

from configuration import GAME_WON_MSG, GAME_LOST_MSG, \
    SLOTS_MIN_WAGER, SLOTS_START_MSG, SLOTS_RESULT_MSG
from .formatting import get_color

from TS3Bot import TS3Bot


REEL_OPTIONS = [option for option in enumerate([
    '\N{grapes}',
    '\N{watermelon}',
    '\N{pineapple}',
    '\N{cherries}',
    '\N{four leaf clover}',
    '\N{rocket}',
    '\N{gem stone}'
    ])]


class Slots:
    MIN_WAGER = SLOTS_MIN_WAGER

    def __init__(self, wager: int):
        self.wager = wager

        reels = [random.choice(REEL_OPTIONS), random.choice(REEL_OPTIONS), random.choice(REEL_OPTIONS)]
        win_ratio = get_win_ratio(reels)

        self.icons = [_icons for _id, _icons in reels]
        self.game_lost = win_ratio == -1
        self.win_amount = self.wager * win_ratio

    def start_round(self, bot: TS3Bot, player_id: int):
        time.sleep(2)
        bot.send_private_message(player_id, SLOTS_START_MSG)
        time.sleep(3)
        bot.send_private_message(player_id, SLOTS_RESULT_MSG)
        bot.send_private_message(player_id, f'| {self.icons[0]} | {self.icons[1]} | {self.icons[2]} |')

        if self.game_lost:
            return bot.send_private_message(player_id, GAME_LOST_MSG.format(self.wager))

        win_amount_color = get_color(self.win_amount)

        return bot.send_private_message(player_id, GAME_WON_MSG.format(win_amount_color, self.win_amount))


def get_win_ratio(reels) -> int:
    ids = [_id for _id, _icons in reels]

    if ids[1] not in [ids[0], ids[2]]:
        return -1

    # average win percentage: 16.32%
    # break-even point win ratio per win: 6.25
    # average win ratio per win: 5.93

    for i in range(0, 7):
        if ids.count(i) != 3:
            continue

        if i == 6:
            return 20  # 0.29% 3 gems
        if i == 5:
            return 10  # 0.29% 3 rockets
        if i == 4:
            return 7  # 0.29% 3 clovers
        return 5  # 1.17% 3 fruits

    i = ids[1]

    if i == 6:
        return 8  # 2.04% 2 gems
    if i == 5:
        return 6  # 2.04% 2 rockets
    if i == 4:
        return 4  # 2.04% 2 clovers

    return 2  # 8.16% 2 fruits
