from configuration import IDLE_MINUTES_BEFORE_AFK, AFK_CHANNELS


class Client:
    def __init__(self, client_id: int, client_info: dict):
        self.id = client_id
        self.db_id = client_info['client_database_id']
        self.uid = client_info['client_unique_identifier']
        self.b64_uid = client_info['client_base64HashClientUID']
        self.name = client_info['client_nickname']
        self.channel_id = client_info['cid']
        self.idle_time = client_info['client_idle_time'] / 1000
        self.is_query = bool(client_info['client_type'])
        self.is_away = bool(client_info['client_away'])
        self.info = client_info

    @property
    def in_afk_channel(self):
        return self.channel_id in AFK_CHANNELS

    @property
    def is_afk(self):
        if self.in_afk_channel:
            return True

        idle_minutes = self.idle_time / 60

        if idle_minutes > IDLE_MINUTES_BEFORE_AFK or self.is_away:
            return True

        return self.is_muted and idle_minutes > IDLE_MINUTES_BEFORE_AFK / 2

    @property
    def is_muted(self):
        input_muted = bool(self.info['client_input_muted'])
        output_muted = bool(self.info['client_output_muted'])
        output_only_muted = bool(self.info['client_outputonly_muted'])
        input_hw_connected = bool(self.info['client_input_hardware'])
        output_hw_connected = bool(self.info['client_output_hardware'])
        return input_muted or output_muted or output_only_muted or not input_hw_connected or not output_hw_connected
