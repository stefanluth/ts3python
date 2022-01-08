from datetime import datetime
import sqlite3

from Client import Client


class SQLiteDB:
    def __init__(self, name):
        self.name = name
        self.connection = sqlite3.connect(f'{self.name}.db', check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        with self.connection:
            try:
                self.cursor.execute(f'CREATE TABLE {self.name} '
                                    f'('
                                    f'database_id text,'
                                    f'unique_id text,'
                                    f'b64_uid text,'
                                    f'nickname text,'
                                    f'measurement_start integer,'
                                    f'connected_total real,'
                                    f'connected_afk real'
                                    f')')
            except sqlite3.OperationalError:
                return

    def create_profile(self, client: Client):
        if self.get_profile(client) is not None:
            return

        with self.connection:
            self.cursor.execute(f'INSERT INTO {self.name} VALUES ('
                                f'"{client.db_id}",'
                                f'"{client.uid}",'
                                f'"{client.b64_uid}",'
                                f'"{client.name}",'
                                f'{int(datetime.now().timestamp())},'
                                f'0.0,'
                                f'0.0)')

        return self.get_profile(client)

    def get_all_profiles(self):
        self.cursor.execute(f'SELECT * FROM {self.name}')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_profile(self, client: Client):
        if client is None:
            return

        self.cursor.execute(f'SELECT * FROM {self.name} '
                            f'WHERE b64_uid="{client.b64_uid}"')
        return dict(self.cursor.fetchone())

    def get_profile_by_b64_uid(self, b64: str):
        self.cursor.execute(f'SELECT * FROM {self.name} '
                            f'WHERE b64_uid="{b64}"')
        return dict(self.cursor.fetchone())

    def get_profile_total(self, client: Client):
        if client is None:
            return
        self.cursor.execute(f'SELECT connected_total '
                            f'FROM {self.name} '
                            f'WHERE b64_uid="{client.b64_uid}"')
        return self.cursor.fetchone()[0]

    def get_profile_total_by_b64_uid(self, b64: str):
        self.cursor.execute(f'SELECT connected_total '
                            f'FROM {self.name} '
                            f'WHERE b64_uid="{b64}"')
        return self.cursor.fetchone()[0]

    def get_profile_afk(self, client: Client):
        if client is None:
            return
        self.cursor.execute(f'SELECT connected_afk '
                            f'FROM {self.name} '
                            f'WHERE b64_uid="{client.b64_uid}"')
        return self.cursor.fetchone()[0]

    def get_profile_afk_by_b64_uid(self, b64: str):
        self.cursor.execute(f'SELECT connected_afk '
                            f'FROM {self.name} '
                            f'WHERE b64_uid="{b64}"')
        return self.cursor.fetchone()[0]

    def update_profile_total(self, client: Client, total: float):
        if client is None:
            return

        with self.connection:
            self.cursor.execute(f'UPDATE {self.name} '
                                f'SET connected_total = {total} '
                                f'WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)

    def update_profile_total_by_b64_uid(self, b64: str, total: float):
        with self.connection:
            self.cursor.execute(f'UPDATE {self.name} '
                                f'SET connected_total = {total} '
                                f'WHERE b64_uid="{b64}"')

        return self.get_profile_by_b64_uid(b64)

    def update_profile_afk(self, client: Client, afk: float):
        if client is None:
            return

        with self.connection:
            self.cursor.execute(f'UPDATE {self.name} '
                                f'SET connected_afk = {afk} '
                                f'WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)

    def update_profile_afk_by_b64_uid(self, b64: str, afk: float):
        with self.connection:
            self.cursor.execute(f'UPDATE {self.name} '
                                f'SET connected_afk = {afk} '
                                f'WHERE b64_uid="{b64}"')

        return self.get_profile_by_b64_uid(b64)
