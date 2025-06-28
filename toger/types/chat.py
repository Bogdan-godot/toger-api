class Chat:
    def __init__(self, chat_id: int, title: str, username: str, _type: str):
        self.id = chat_id
        self.title = title
        self.username = username
        self.type = _type