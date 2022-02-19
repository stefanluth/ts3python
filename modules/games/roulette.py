import random
import time

from .configuration import ROULETTE_MIN_WAGER, ROULETTE_START_MSG, ROULETTE_RESULT_MSG, GAME_LOST_MSG, GAME_WON_MSG
from modules.games.formatting import get_color
from ts3bot import TS3Bot

BETS = {
    'low': {'name': 'Low',
            'numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            'ratio': 2},
    'high': {'name': 'High',
             'numbers': [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
             'ratio': 2},
    'odd': {'name': 'Odd',
            'numbers': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35],
            'ratio': 2},
    'even': {'name': 'Even',
             'numbers': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36],
             'ratio': 2},
    'red': {'name': 'Red',
            'numbers': [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
            'ratio': 2},
    'black': {'name': 'Black',
              'numbers': [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
              'ratio': 2},
    'col1': {'name': '1st Column',
             'numbers': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
             'ratio': 3},
    'col2': {'name': '2nd Column',
             'numbers': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
             'ratio': 3},
    'col3': {'name': '3rd Column',
             'numbers': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
             'ratio': 3},
    'doz1': {'name': '1st Dozen',
             'numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
             'ratio': 3},
    'doz2': {'name': '2nd Dozen',
             'numbers': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
             'ratio': 3},
    'doz3': {'name': '3rd Dozen',
             'numbers': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
             'ratio': 3},
    'snake': {'name': 'Snake',
              'numbers': [1, 5, 9, 12, 14, 16, 19, 23, 27, 30, 32, 34],
              'ratio': 3},
    'basket': {'name': 'Basket',
               'numbers': [0, 1, 2, 3],
               'ratio': 9},
}


class Roulette:
    VALID_BETS = list(BETS.keys()) + [str(i) for i in range(0, 37)]
    MIN_WAGER = ROULETTE_MIN_WAGER

    def __init__(self, wager: int, bet: str):
        self.wager = wager

        try:
            numbers_bet_on = [int(bet)]
            win_ratio = 36
            self.bet = bet
        except ValueError:
            numbers_bet_on = BETS[bet]['numbers']
            win_ratio = BETS[bet]['ratio']
            self.bet = BETS[bet]['name']

        self.winning_number = random.randint(0, 36)
        self.game_lost = self.winning_number not in numbers_bet_on

        if self.game_lost:
            win_ratio = -1

        self.win_amount = wager * win_ratio

    def start_round(self, bot: TS3Bot, player_id: int):
        time.sleep(2)
        bot.send_private_message(player_id, ROULETTE_START_MSG.format(self.wager, self.bet))
        time.sleep(3)
        bot.send_private_message(player_id, ROULETTE_RESULT_MSG.format(self.winning_number))

        if self.game_lost:
            return bot.send_private_message(player_id, GAME_LOST_MSG.format(self.wager))

        win_amount_color = get_color(self.win_amount)

        return bot.send_private_message(player_id, GAME_WON_MSG.format(win_amount_color, self.win_amount))
