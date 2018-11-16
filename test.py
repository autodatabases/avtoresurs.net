from typing import Iterable


class MessagePattern:
    def __init__(self):
        self.user = self.User()
        self.channel = ""
        self.sn_channel_id = ""
        self.message = ""
        self.attachments = []

    class User:
        def __init__(self):
            self.id = None
            self.first_name = None
            self.last_name = None
            self.username = None

    def as_dict(self):
        return dict(vars(self), user=vars(self.user))


test = MessagePattern()

print(test.as_dict())