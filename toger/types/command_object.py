class CommandObject:
    def __init__(self, text_message: str):
        self.args = " ".join(text_message.split()[1:])
        self.args_list = text_message.split()[1:]