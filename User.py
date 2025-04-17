
class User:
    def __init__(self, clientObj=None, nickname=None, message=None):
        self.clientObj = clientObj
        self.nickname = nickname
        self.message = message

    def __str__(self):
        return f"{self.nickname}:{self.message}"