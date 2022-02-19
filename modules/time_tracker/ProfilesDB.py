from sqlite3 import OperationalError
import time

from Client import Client
from SQLiteDB import SQLiteDB


class ProfilesDB(SQLiteDB):
    def __init__(self, name):
        super().__init__(name)
        try:
            self.create_table()
        except OperationalError as error:
            if str(error) == f'table {self.name} already exists':
                pass
            else:
                raise error

    def create_table(self):
        self.execute(f'CREATE TABLE {self.name} (database_id text,'
                     f'unique_id text,'
                     f'b64_uid text,'
                     f'nickname text,'
                     f'measurement_start integer,'
                     f'connected_total real,'
                     f'connected_afk real,'
                     f'do_not_track boolean)')

    def create_profile(self, client: Client):
        if self.get_profile(client) is not None:
            return

        self.execute(f'INSERT INTO {self.name} VALUES ('
                     f'"{client.db_id}",'
                     f'"{client.uid}",'
                     f'"{client.b64_uid}",'
                     f'"{client.name}",'
                     f'{int(time.time())},'
                     f'0.0,'
                     f'0.0,'
                     f'false)')

        return self.get_profile(client)

    def get_all_profiles(self):
        self.execute(f'SELECT * FROM {self.name}')

        return self.fetch_all()

    def get_profile(self, client: Client):
        self.execute(f'SELECT * FROM {self.name} WHERE b64_uid="{client.b64_uid}"')

        return self.fetch_one_dict()

    def get_profile_total(self, client: Client):
        self.execute(f'SELECT connected_total FROM {self.name} WHERE b64_uid="{client.b64_uid}"')

        return self.fetch_one()

    def get_profile_afk(self, client: Client):
        self.execute(f'SELECT connected_afk FROM {self.name} WHERE b64_uid="{client.b64_uid}"')

        return self.fetch_one()

    def update_profile_total(self, client: Client, total: float):
        self.execute(f'UPDATE {self.name} SET connected_total = {total} WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)

    def update_profile_afk(self, client: Client, afk: float):
        self.execute(f'UPDATE {self.name} SET connected_afk = {afk} WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)

    def set_do_not_track(self, uid: str, do_not_track: bool):
        self.execute(f'UPDATE {self.name} SET do_not_track = {do_not_track} WHERE unique_id="{uid}"')

    def toggle_do_not_track(self, uid: str):
        toggled = not self.get_do_not_track(uid)
        self.set_do_not_track(uid, toggled)

        return toggled

    def get_do_not_track(self, uid: str):
        self.execute(f'SELECT do_not_track FROM {self.name} WHERE unique_id="{uid}"')

        return self.fetch_one()
