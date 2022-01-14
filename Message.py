msg_types = {
    1: 'private',
    2: 'channel',
    3: 'server',
}


class Message:
    def __init__(self, message: dict):
        self.invoker_name: str = message['invokername']
        self.invoker_id: int = message['invokerid']
        self.invoker_uid: str = message['invokeruid']
        self.type: str = msg_types[message['targetmode']]
        self.content: str = self.parse_content(str(message['msg']))
        self.raw = message
        self.used = False

    @staticmethod
    def parse_content(message: str):
        return message.replace(r'\s', ' ').strip()

    def mark_as_used(self):
        self.used = True
