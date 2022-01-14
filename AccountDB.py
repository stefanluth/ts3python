from sqlite3 import OperationalError
from SQLiteDB import SQLiteDB


class AccountDB(SQLiteDB):
    def _init__(self, name):
        super().__init__(name)
        try:
            self._create_table()
        except OperationalError as error:
            if str(error) == f'table {self.name} already exists':
                pass
            else:
                raise error

    def update_balance_after_game(self, uid: str, amount: int) -> int:
        old_balance = self.get_balance(uid)
        new_balance = old_balance + amount

        self._add_games_played(uid)

        if amount > 0:
            self._add_win(uid)
            self._check_biggest_win(uid, amount)
        elif amount < 0:
            self._add_loss(uid)
            self._check_biggest_loss(uid, amount)

        return self.set_balance(uid, new_balance)

    def update_balance(self, uid: str, amount: int) -> int:
        old_balance = self.get_balance(uid)
        new_balance = old_balance + amount

        return self.set_balance(uid, new_balance)

    def _add_win(self, uid: str) -> int:
        old_wins = self.get_wins(uid)
        new_wins = old_wins + 1

        streak = self.get_streak(uid)

        if streak >= 0:
            new_streak = streak + 1
            self._set_streak(uid, new_streak)
            best_streak = self.get_best_streak(uid)
            new_best_streak = new_streak > best_streak
            if new_best_streak:
                self._set_best_streak(uid, new_streak)
        else:
            self._set_streak(uid, 1)

        return self._set_wins(uid, new_wins)

    def _add_loss(self, uid: str) -> int:
        old_losses = self.get_losses(uid)
        new_losses = old_losses + 1

        streak = self.get_streak(uid)

        if streak <= 0:
            new_streak = streak - 1
            self._set_streak(uid, new_streak)
            worst_streak = self.get_worst_streak(uid)
            new_worst_streak = new_streak < worst_streak
            if new_worst_streak:
                self._set_worst_streak(uid, new_streak)
        else:
            self._set_streak(uid, -1)

        return self._set_losses(uid, new_losses)

    def _add_games_played(self, uid: str) -> int:
        old_games_played = self.get_games_played(uid)
        new_games_played = old_games_played + 1

        return self._set_games_played(uid, new_games_played)

    def _check_biggest_win(self, uid, amount):
        biggest_win = self.get_biggest_win(uid)
        new_biggest_win = amount > biggest_win
        if new_biggest_win:
            self._set_biggest_win(uid, amount)

    def _check_biggest_loss(self, uid, amount):
        biggest_loss = self.get_biggest_loss(uid)
        new_biggest_loss = amount < biggest_loss
        if new_biggest_loss:
            self._set_biggest_loss(uid, amount)

    def get_balance(self, uid) -> int:
        self.execute(f'SELECT balance FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def set_balance(self, uid: str, amount: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET balance = {amount} '
                     f'WHERE uid="{uid}"')
        return self.get_balance(uid)

    def get_wins(self, uid: str) -> int:
        self.execute(f'SELECT wins FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def get_losses(self, uid: str) -> int:
        self.execute(f'SELECT losses FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def get_streak(self, uid: str) -> int:
        self.execute(f'SELECT streak FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def get_best_streak(self, uid: str) -> int:
        self.execute(f'SELECT best_streak FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def get_worst_streak(self, uid: str) -> int:
        self.execute(f'SELECT worst_streak FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def get_biggest_win(self, uid: str) -> int:
        self.execute(f'SELECT biggest_win FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def get_biggest_loss(self, uid: str) -> int:
        self.execute(f'SELECT biggest_loss FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def get_account(self, uid: str):
        self.execute(f'SELECT * FROM {self.name} '
                     f'WHERE uid="{uid}"')

        return self.fetch_one()

    def get_all_accounts(self):
        self.execute(f'SELECT * FROM {self.name}')

        return self.fetch_all()

    def create_account(self, uid: str):
        if self.get_account(uid) is not None:
            return

        self.execute(f'INSERT INTO {self.name} VALUES ('
                     f'"{uid}", '
                     f'5000, '
                     f'0, 0, 0, 0, 0, 0, 0, 0'
                     f')')

    def _create_table(self):
        self.execute(f'CREATE TABLE {self.name} ('
                     f'uid text,'
                     f'balance integer,'
                     f'wins integer,'
                     f'losses integer,'
                     f'streak integer,'
                     f'best_streak integer,'
                     f'worst_streak integer,'
                     f'games_played integer,'
                     f'biggest_win integer,'
                     f'biggest_loss integer'
                     f')')

    def _set_wins(self, uid: str, wins: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET wins = {wins} '
                     f'WHERE uid="{uid}"')
        return self.get_wins(uid)

    def _set_losses(self, uid: str, losses: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET losses = {losses} '
                     f'WHERE uid="{uid}"')
        return self.get_losses(uid)

    def _set_streak(self, uid: str, streak: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET streak = {streak} '
                     f'WHERE uid="{uid}"')
        return self.get_streak(uid)

    def _set_best_streak(self, uid: str, streak: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET best_streak = {streak} '
                     f'WHERE uid="{uid}"')
        return self.get_best_streak(uid)

    def _set_worst_streak(self, uid: str, streak: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET worst_streak = {streak} '
                     f'WHERE uid="{uid}"')
        return self.get_worst_streak(uid)

    def get_games_played(self, uid: str) -> int:
        self.execute(f'SELECT games_played FROM {self.name} '
                     f'WHERE uid="{uid}"')
        return self.fetch_one()

    def _set_games_played(self, uid: str, games: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET games_played = {games} '
                     f'WHERE uid="{uid}"')
        return self.get_games_played(uid)

    def _set_biggest_win(self, uid: str, amount: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET biggest_win = {amount} '
                     f'WHERE uid="{uid}"')
        return self.get_biggest_win(uid)

    def _set_biggest_loss(self, uid: str, amount: int) -> int:
        self.execute(f'UPDATE {self.name} '
                     f'SET biggest_loss = {amount} '
                     f'WHERE uid="{uid}"')
        return self.get_biggest_loss(uid)
