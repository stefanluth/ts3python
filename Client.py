from configuration import IDLE_MINUTES_BEFORE_AFK, AFK_CHANNELS
from TS3Bot import TS3Bot


class Client:
    def __init__(self, client_id: int, client_info: dict):
        self.id = client_id
        self.db_id = client_info['client_database_id']
        self.uid = client_info['client_unique_identifier']
        self.b64_uid = client_info['client_base64HashClientUID']
        self.name = client_info['client_nickname']
        self.channel_id = client_info['cid']
        self.is_query = bool(client_info['client_type'])
        self.info = client_info

    @property
    def in_afk_channel(self):
        return self.channel_id in AFK_CHANNELS

    @property
    def is_afk(self):
        if self.in_afk_channel:
            return True

        idle_time_in_seconds = self.info['client_idle_time'] / 1000
        idle_time_in_minutes = idle_time_in_seconds / 60
        is_away = bool(self.info['client_away'])

        if idle_time_in_minutes > IDLE_MINUTES_BEFORE_AFK or is_away:
            return True

        input_muted = bool(self.info['client_input_muted'])
        output_muted = bool(self.info['client_output_muted'])
        output_only_muted = bool(self.info['client_outputonly_muted'])
        input_hw_connected = bool(self.info['client_input_hardware'])
        output_hw_connected = bool(self.info['client_output_hardware'])

        is_muted = input_muted or output_muted or output_only_muted or not input_hw_connected or not output_hw_connected

        return is_muted and idle_time_in_minutes > IDLE_MINUTES_BEFORE_AFK / 2

    def move(self, bot: TS3Bot, channel_id):
        return bot.move_client(self.id, channel_id)

    def kick_from_channel(self, bot: TS3Bot, reason: str):
        return bot.kick_client_from_channel(self.id, reason)

    def kick_from_server(self, bot: TS3Bot, reason: str):
        return bot.kick_client_from_server(self.id, reason)

    def ban(self, bot: TS3Bot, duration: int, reason: str):
        return bot.ban_client(self.id, duration, reason)
