from datetime import datetime
import sqlite3
import threading

from Client import Client


class SQLiteDB:
    def __init__(self, name):
        self.name = name
        self.connection = sqlite3.connect(f'{self.name}.db', check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.lock = threading.Lock()

        try:
            # This column was added late. This ensures backwards compatibility.
            self.execute(f'alter table {self.name} add do_not_track boolean default false;')
        except sqlite3.OperationalError as error:
            if str(error) == 'duplicate column name: do_not_track' or str(error) == f'no such table: {self.name}':
                pass
            else:
                raise error

        try:
            self.create_table()
        except sqlite3.OperationalError as error:
            if str(error) == 'table profiles already exists':
                pass
            else:
                raise error

    def create_table(self):
        self.execute(f'CREATE TABLE {self.name} ('
                     f'database_id text,'
                     f'unique_id text,'
                     f'b64_uid text,'
                     f'nickname text,'
                     f'measurement_start integer,'
                     f'connected_total real,'
                     f'connected_afk real,'
                     f'do_not_track boolean'
                     f')')

    def execute(self, query):
        with self.lock:
            with self.connection:
                self.cursor.execute(query)

    def fetch_all(self):
        with self.lock:
            result = [dict(row) for row in self.cursor.fetchall()]

        return result

    def fetch_one(self):
        with self.lock:
            result = self.cursor.fetchone()[0]

        return result

    def create_profile(self, client: Client):
        if self.get_profile(client) != dict():
            return

        self.execute(f'INSERT INTO {self.name} VALUES ('
                     f'"{client.db_id}", '
                     f'"{client.uid}", '
                     f'"{client.b64_uid}", '
                     f'"{client.name}", '
                     f'{int(datetime.now().timestamp())}, '
                     f'0.0, '
                     f'0.0, '
                     f'false'
                     f')')

        return self.get_profile(client)

    def get_all_profiles(self):
        self.execute(f'SELECT * FROM {self.name}')

        return self.fetch_all()

    def get_profile(self, client: Client):
        if client is None:
            return

        self.execute(f'SELECT * FROM {self.name} '
                     f'WHERE b64_uid="{client.b64_uid}"')

        try:
            return dict(self.cursor.fetchone())
        except TypeError:
            return dict()

    def get_profile_total(self, client: Client):
        if client is None:
            return

        self.execute(f'SELECT connected_total '
                     f'FROM {self.name} '
                     f'WHERE b64_uid="{client.b64_uid}"')

        return self.fetch_one()

    def get_profile_afk(self, client: Client):
        if client is None:
            return

        self.execute(f'SELECT connected_afk '
                     f'FROM {self.name} '
                     f'WHERE b64_uid="{client.b64_uid}"')

        return self.fetch_one()

    def update_profile_total(self, client: Client, total: float):
        if client is None:
            return

        self.execute(f'UPDATE {self.name} '
                     f'SET connected_total = {total} '
                     f'WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)

    def update_profile_afk(self, client: Client, afk: float):
        if client is None:
            return

        self.execute(f'UPDATE {self.name} '
                     f'SET connected_afk = {afk} '
                     f'WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)

    def set_do_not_track(self, client: Client, do_not_track: bool):
        if client is None:
            return

        self.execute(f'UPDATE {self.name} '
                     f'SET do_not_track = {do_not_track} '
                     f'WHERE b64_uid="{client.b64_uid}"')

    def toggle_do_not_track(self, client: Client):
        if client is None:
            return

        toggled = not self.get_do_not_track(client)
        self.set_do_not_track(client, toggled)

        return toggled

    def get_do_not_track(self, client: Client):
        if client is None:
            return

        self.execute(f'SELECT do_not_track '
                     f'FROM {self.name} '
                     f'WHERE b64_uid="{client.b64_uid}"')

        return self.fetch_one()
