import telnetlib
import threading


class TS3Query:
    """
    The telnet connection to the server query interface.
    """
    def __init__(self, ip='', port=40014):
        """
        :param ip: TS3 server IP address.
        :param port: TS3 telnet port.
        """
        self.telnet = telnetlib.Telnet(host=ip, port=port)
        self._skip_welcome_msg()
        self.host = ip
        self.port = port
        self.lock = threading.Lock()

    def login(self, login: str, password: str):
        return self.send(f'login {login} {password}')

    def use(self, server_id=0, port=0):
        if port:
            return self.send(f'use port={port}')
        return self.send(f'use {server_id}')

    def logout(self):
        return self.send('logout')

    def quit(self):
        return self.send('quit')

    def exit(self):
        self.logout()
        self.quit()

    def send(self, command: str):
        self.lock.acquire()
        encoded_command: bytes = f'{command.strip()}\n'.encode()
        self.telnet.write(encoded_command)
        response = self.receive()
        self.lock.release()
        return response

    def receive(self):
        _index, error_id_msg, response_text = self.telnet.expect([br'error id=\d{1,4} msg=.+\n\r'])
        response_text_string = response_text.decode().strip()
        response_dict = self.parse_response(response_text_string)
        return response_dict

    @classmethod
    def parse_response(cls, response: str):
        if response.startswith('error id='):
            return dict()

        response = response.split('\n\rerror id=')[0]
        response_entries = response.split('|')

        if len(response_entries) > 1:
            dict_list = [cls.dict_from_list(response_entry.split()) for response_entry in response_entries]
            return dict_list

        response_list = response.split()
        return cls.dict_from_list(response_list)

    @staticmethod
    def dict_from_list(keys_values: list):
        response_dict = dict()

        for key_value_pair in keys_values:
            key = key_value_pair.split('=')[0]
            value = key_value_pair[len(key)+1:]
            try:
                response_dict[key] = int(value)
            except ValueError:
                response_dict[key] = value.strip()

        return response_dict

    def _skip_welcome_msg(self):
        self.telnet.read_until(b'TS3\n\rWelcome to the TeamSpeak 3 ServerQuery interface, type "help" for a list of '
                               b'commands and "help <command>" for information on a specific command.\n\r')
