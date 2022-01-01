import telnetlib
import threading


class TS3Query:
    def __init__(self, ip='', port=40014):
        """
        :param ip: TeamSpeak 3 Server IP Address.
        :param port: Telnet Port to Given TeamSpeak 3 Server.
        """
        self.telnet = telnetlib.Telnet(host=ip, port=port)
        self._ignore_welcome_msg()
        self.host = ip
        self.port = port
        self.lock = threading.Lock()

    def login(self, login: str, password: str):
        return self.send(f'login {login} {password}')

    def logout(self):
        return self.send('logout')

    def send(self, command: str):
        encoded_command: bytes = f'{command.strip()}\n'.encode()
        self.telnet.write(encoded_command)
        return self.receive()

    def receive(self):
        match_index, match_object, match_text = self.telnet.expect([br'error id=\d{1,4} msg=.+\n\r'])
        match_text_string = match_text.decode().strip()
        return match_text_string

    def _ignore_welcome_msg(self):
        self.telnet.read_until(b'TS3\n\rWelcome to the TeamSpeak 3 ServerQuery interface, type "help" for a list of '
                               b'commands and "help <command>" for information on a specific command.\n\r')
