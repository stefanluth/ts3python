from configuration import AFK_CHANNELS
from TS3Bot import TS3Bot


class Channel:
    def __init__(self, channel_id: int, channel_info: dict):
        self.id = channel_id
        self.name = channel_info['channel_name']
        self.phonetic_name = channel_info['channel_name_phonetic']
        self.banner_image_url = channel_info['channel_banner_gfx_url']
        self.description = channel_info['channel_description']
        self.topic = channel_info['channel_topic']
        self.unique_id = channel_info['channel_unique_identifier']
        self.file_path = channel_info['channel_filepath']

        self.icon_id = channel_info['channel_icon_id']
        self.needed_talk_power = channel_info['channel_needed_talk_power']
        self.parent_id = channel_info['pid']
        self.seconds_empty = channel_info['seconds_empty']
        self.order = channel_info['channel_order']

        self.is_permanent = bool(channel_info['channel_flag_permanent'])
        self.is_semi_permanent = bool(channel_info['channel_flag_semi_permanent'])
        self.is_default = bool(channel_info['channel_flag_default'])
        self.has_password = bool(channel_info['channel_flag_password'])

    def rename(self, bot: TS3Bot, name: str):
        return bot.rename_channel(self.id, name)

    def set_description(self, bot: TS3Bot, description: str):
        return bot.set_channel_description(self.id, description)

    def edit(self, bot: TS3Bot, parameters: dict):
        return bot.edit_channel(self.id, parameters)

    @property
    def is_afk_channel(self):
        return self.id in AFK_CHANNELS
