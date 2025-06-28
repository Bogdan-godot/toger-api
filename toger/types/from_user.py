from datetime import datetime


class From_user:
    def __init__(self, user_id: int, first_name: str, username: str, is_bot: bool, date: datetime):
        self.first_name = first_name
        self.id = user_id
        self.username = username
        self.is_bot = is_bot
