from credentials import *
from TS3Query import TS3Query


def dict_to_parameters(parameters: dict):
    return r'\s'.join([f'{key}={format_value(value)}' for key, value in parameters.items()])


def format_value(value: str):
    return r'\s'.join(value.split())


class TS3Bot:
    """
    An interface to send commands to the server.
    """
    def __init__(self):
        self.connection = TS3Query(SERVER_IP, TELNET_PORT)
        self.connection.login(TELNET_LOGIN, TELNET_PW)
        self.connection.use(port=SERVER_PORT)
        self.client_id = self.whoami()['client_id']

    def exit(self):
        self.connection.exit()

    def whoami(self):
        return self.connection.send('whoami')

    def set_bot_description(self, description: str):
        return self.update_client_description(self.client_id, description)

    def set_bot_name(self, name: str):
        return self.update_client(self.client_id, {'client_nickname': name})

    def get_client_list(self):
        return self.connection.send('clientlist')

    def get_client_id_from_uid(self, client_uid: str):
        return self.connection.send(f'clientgetids cluid={client_uid}')

    def get_client_dbid_from_uid(self, client_uid: str):
        return self.connection.send(f'clientgetdbidfromuid cluid={client_uid}')

    def get_client_uid_from_id(self, client_id: int):
        return self.connection.send(f'clientgetuidfromclid clid={client_id}')

    def get_client_info(self, client_id: int):
        return self.connection.send(f'clientinfo clid={client_id}')

    def update_client(self, client_id: int, parameters: dict):
        parameters_string = dict_to_parameters(parameters)
        return self.connection.send(f'clientupdate clid={client_id} {parameters_string}')

    def update_client_description(self, client_id: int, description: str):
        formatted_description = format_value(description)
        return self.connection.send(f'clientedit clid={client_id} client_description={formatted_description}')

    def poke_client(self, client_id: int, msg: str):
        formatted_message = format_value(msg)
        return self.connection.send(f'clientpoke clid={client_id} msg={formatted_message}')

    def move_client(self, client_id: int, channel_id: int):
        return self.connection.send(f'clientmove clid={client_id} cid={channel_id}')

    def send_server_message(self, msg: str):
        formatted_message = format_value(msg)
        return self.connection.send(f'sendtextmessage targetmode=3 msg={formatted_message}')

    def send_channel_message(self, msg: str):
        formatted_message = format_value(msg)
        return self.connection.send(f'sendtextmessage targetmode=2 msg={formatted_message}')

    def send_private_message(self, client_id: int, msg: str):
        formatted_message = format_value(msg)
        return self.connection.send(f'sendtextmessage targetmode=1 target={client_id} msg={formatted_message}')

    def set_welcome_message(self, msg: str):
        formatted_message = format_value(msg)
        return self.connection.send(f'serveredit virtualserver_welcomemessage={formatted_message}')

    def set_new_host_message(self, msg: str):
        formatted_host_message = format_value(msg)
        return self.connection.send(f'serveredit virtualserver_hostmessage={formatted_host_message}')

    def set_host_message_mode(self, mode: int):
        if 0 > mode > 3:
            return
        return self.connection.send(f'serveredit virtualserver_hostmessage_mode={mode}')

    def reset_host_message(self):
        self.set_host_message_mode(0)
        return self.set_new_host_message('')

    def change_host_banner_image(self, image_url: str):
        return self.connection.send(f'serveredit virtualserver_hostbanner_gfx_url={image_url}')