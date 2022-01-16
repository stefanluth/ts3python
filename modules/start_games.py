import time
import threading

from Message import Message
from configuration import GAME_INVALID_CMD, GAME_INVALID_AMOUNT, GAME_INVALID_GAME, GAME_GREETINGS, \
    GAME_ABORT_BROKE, GAME_ABORT_BAD_WAGER, GAME_ABORT_BAD_BET, ACCOUNT_INFO_BALANCE
from .games.Slots import Slots
from .games.Roulette import Roulette

from AccountDB import AccountDB
from TS3Bot import TS3Bot

GAMES = ['slots', 'roulette']


def start_games(bot: TS3Bot, database: AccountDB):
    current_games = list()
    while 1:
        for message in bot.unused_messages:
            current_games = [[_id, _thread] for _id, _thread in current_games if _thread.is_alive()]
            already_playing = message.invoker_id in [_id for _id, _thread in current_games]

            if already_playing:
                message.mark_as_used()
                continue

            if message.content.startswith('!balance'):
                balance = database.get_balance(message.invoker_uid)
                bot.send_private_message(message.invoker_id, ACCOUNT_INFO_BALANCE.format(balance))
                message.mark_as_used()
                continue

            if not message.content.startswith('!play'):
                continue

            message.mark_as_used()

            if database.get_account(message.invoker_uid) is None:
                database.create_account(message.invoker_uid)

            try:
                command, game_name, wager, *args = message.content.split()
            except ValueError:
                bot.send_private_message(message.invoker_id, GAME_INVALID_CMD)
                continue

            if game_name.lower() not in GAMES:
                bot.send_private_message(message.invoker_id, GAME_INVALID_GAME)
                continue

            try:
                wager = int(wager)
            except ValueError:
                bot.send_private_message(message.invoker_id, GAME_INVALID_AMOUNT)
                continue

            player_is_broke = wager > database.get_balance(message.invoker_uid)

            if player_is_broke:
                bot.send_private_message(message.invoker_id, GAME_ABORT_BROKE)
                continue

            bot.send_private_message(message.invoker_id, GAME_GREETINGS.format(message.invoker_name))

            player_id, player_thread = choose_game(bot, database, game_name, wager, message, args)
            current_games.append([player_id, player_thread])

        time.sleep(1)


def choose_game(bot: TS3Bot, database: AccountDB, game: str, wager: int, message: Message, args: list):
    if game == 'slots':
        roulette_min_web = Slots.MIN_WAGER
        wager_too_low = wager < roulette_min_web

        if wager_too_low:
            bot.send_private_message(message.invoker_id, GAME_ABORT_BAD_WAGER.format(roulette_min_web))
            return [message.invoker_id, threading.Thread()]

        slots_game = Slots(wager)
        database.update_balance_after_game(message.invoker_uid, slots_game.win_amount)
        slots_thread = threading.Thread(target=slots_game.start_round,
                                        kwargs={
                                            'bot': bot,
                                            'player_id': message.invoker_id,
                                        })
        slots_thread.start()
        return [message.invoker_id, slots_thread]

    if game == 'roulette':
        roulette_min_web = Roulette.MIN_WAGER
        wager_too_low = wager < roulette_min_web

        if wager_too_low:
            bot.send_private_message(message.invoker_id, GAME_ABORT_BAD_WAGER.format(roulette_min_web))
            return [message.invoker_id, threading.Thread()]

        if len(args) != 1:
            return [message.invoker_id, threading.Thread()]

        bet = args[0]
        invalid_bet = bet not in Roulette.VALID_BETS

        if invalid_bet:
            bot.send_private_message(message.invoker_id, GAME_ABORT_BAD_BET)
            return [message.invoker_id, threading.Thread()]

        roulette_game = Roulette(wager, bet)
        database.update_balance_after_game(message.invoker_uid, roulette_game.win_amount)
        roulette_thread = threading.Thread(target=roulette_game.start_round,
                                           kwargs={
                                               'bot': bot,
                                               'player_id': message.invoker_id,
                                           })
        roulette_thread.start()
        return [message.invoker_id, roulette_thread]
