class DiceObject:
    def __init__(self, obj: dict):
        self.__dice = obj.get("dice", {})
        self.emoji = self.__dice.get("emoji", None)
        self.value = self.__dice.get("value", None)