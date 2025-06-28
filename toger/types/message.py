from datetime import datetime
from typing import Optional, Union, Literal
import asyncio

# from .reply_to_message import Reply_to_message
from .from_user import From_user
# from .chat import Chat
# from .dice_object import DiceObject
from .. import base, loggers


class MessageObject:
    def __init__(self, auth_string: str, type: Literal["message_new"],
                 user_id: int, chat_id: int, message_id: int, message_text: str, date: datetime
                 ):
        self.__auth_string = auth_string

        self.type: Literal["message_new"] = type

        self.chat_id = chat_id
        self.__user_id = user_id

        self.from_user: From_user = None

        self.message_id = message_id
        self.text = message_text

        self.date = date

    @classmethod
    async def create(cls, auth_string: str, type: Literal["message_new"],
                     user_id: int, chat_id: int, message_id: int, message_text: str, date: datetime):
        instance = cls(auth_string, type, user_id, chat_id,
                       message_id, message_text, date)
        from ..methods.get_user import GetUser
        instance.from_user = await GetUser(auth_string, user_id)()
        return instance

    async def answer(self, message: str):
        from ..methods import SendMessage
        call = SendMessage(
            auth_string=self.__auth_string,
            chat_id=self.chat_id,
            text=message
        )

        return await call()

    # async def reply(self, message: str, parse_mode: str="HTML", reply_markup=None):
    #     if not isinstance(parse_mode, str):
    #         loggers.event.error(f"Expected 'parse_mode' to be a string, got {type(parse_mode).__name__}")
    #         return False
    #     if not isinstance(message, str):
    #         loggers.event.error(f"Expected 'message' to be a string, got {type(message).__name__}")
    #         return False
    #     if message == "" and message == None:
    #         loggers.event.error("The message is empty.")
    #         return False

    #     payload = {
    #         "chat_id": self.__chat_id,
    #         "text": message,
    #         "reply_to_message_id": self.message_id,
    #         "parse_mode": parse_mode
    #     }

    #     if reply_markup:
    #         payload["reply_markup"] = reply_markup

    #     try:
    #         async with self.session.post(self.__url + "sendMessage", json=payload) as response:
    #             response.raise_for_status()
    #             data = await response.json()
    #             loggers.event.info("The message has been sent successfully.")
    #             return True
    #     except Exception as e:
    #         loggers.event.error(f"{e}")
    #         return False

    # async def delete_message(self) -> bool:
    #     payload = {
    #         "chat_id": self.__chat_id,
    #         "message_id": self.message_id,
    #     }
    #     try:
    #         async with self.session.post(self.__url + "deleteMessage", json=payload) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 return True
    #             else:
    #                 raise TogerBadRequest((await response.json()).get("description"))
    #     except Exception as e:
    #         loggers.event.error(f"{e}")
    #         return False

    # async def reply_photo(self, file_path: str=None, url_photo: str=None, caption: str = None, parse_mode: str="HTML", reply_markup=None):
    #     if not isinstance(parse_mode, str):
    #         raise ValueError("The 'parse_mode' parameter cannot be None or not a string.")

    #     if not isinstance(url_photo, str):
    #         raise ValueError("The 'url_photo' parameter cannot be None or not a string.")

    #     try:
    #         if file_path:
    #             # Чтение файла и создание FormData
    #             with open(file_path, "rb") as photo_file:
    #                 form_data = aiohttp.FormData()
    #                 form_data.add_field("chat_id", str(self.__chat_id))
    #                 form_data.add_field("photo", photo_file, filename=file_path.split("/")[-1])
    #                 form_data.add_field("parse_mode", parse_mode)
    #                 form_data.add_field("reply_to_message_id", self.message_id)
    #         else:
    #             form_data = aiohttp.FormData()
    #             form_data.add_field("chat_id", str(self.__chat_id))
    #             form_data.add_field("photo", url_photo)
    #             form_data.add_field("parse_mode", parse_mode)
    #             form_data.add_field("reply_to_message_id", self.message_id)

    #         if caption:
    #             form_data.add_field("caption", caption)

    #         if reply_markup:
    #             form_data.add_field("reply_markup", reply_markup)

    #         # Отправка запроса
    #         async with self.session.post(f"{self.__url}sendPhoto", data=form_data) as response:
    #             response.raise_for_status()  # Бросает исключение при HTTP-ошибке
    #             loggers.event.info("The photo was successfully sent.")
    #             data = await response.json()
    #             return True

    #     except aiohttp.ClientError as e:
    #         loggers.event.error(f"ERROR: {e}")
    #         return False

    #     except FileNotFoundError:
    #         loggers.event.error(f"ERROR: File not found: {file_path}")
    #         return False

    # async def answer_photo(self, file_path: str=None, url_photo: str=None, caption: str = None, parse_mode: str="HTML", reply_markup=None):
    #     if not isinstance(parse_mode, str):
    #         loggers.event.error(f"Expected 'parse_mode' to be a string, got {type(parse_mode).__name__}")
    #         return False

    #     if not isinstance(url_photo, str):
    #         loggers.event.error(f"Expected 'url_photo' to be a string, got {type(url_photo).__name__}")
    #         return False

    #     try:
    #         if file_path:
    #             # Чтение файла и создание FormData
    #             with open(file_path, "rb") as photo_file:
    #                 form_data = aiohttp.FormData()
    #                 form_data.add_field("chat_id", str(self.__chat_id))
    #                 form_data.add_field("photo", photo_file, filename=file_path.split("/")[-1])
    #                 form_data.add_field("parse_mode", parse_mode)
    #         else:
    #             form_data = aiohttp.FormData()
    #             form_data.add_field("chat_id", str(self.__chat_id))
    #             form_data.add_field("photo", url_photo)
    #             form_data.add_field("parse_mode", parse_mode)

    #         if caption:
    #             form_data.add_field("caption", caption)

    #         if reply_markup:
    #             form_data.add_field("reply_markup", reply_markup)

    #         # Отправка запроса
    #         async with self.session.post(f"{self.__url}sendPhoto", data=form_data) as response:
    #             response.raise_for_status()  # Бросает исключение при HTTP-ошибке
    #             loggers.event.info("The photo was successfully sent.")
    #             data = await response.json()
    #             return True

    #     except aiohttp.ClientError as e:
    #         loggers.bot.error(f"ERROR: {e}")
    #         return False

    #     except FileNotFoundError:
    #         loggers.bot.error(f"ERROR: File not found: {file_path}")
    #         return False

    # async def edit_text(self, text: str):
    #     if not isinstance(text, str):
    #         raise ValidationError(f"Expected 'text' to be a string, got {type(text).__name__}")
    #         return
    #     payload = {
    #         "chat_id": self.__chat_id,
    #         "message_id": self.message_id,
    #         "text": text
    #     }

    #     try:
    #         async with self.session.post(self.__url + "editMessageText", json=payload) as response:
    #             if response.status == 200:
    #                 data = (await response.json()).get("result")
    #                 data_from = data.get("from")
    #                 data_chat = data.get("chat")
    #                 return MessageObject(message_id=int(data.get("message_id")), fullname=data_from.get("fullname"), username=data_from.get("username"),
    #                                     is_bot=data_from.get("is_bot"), message_text=data.get("text"), user_id=data_from.get("id"),
    #                                     chat_id=data_chat.get("id"), type_chat=data_chat.get("type"), title=data_chat.get("title", None), chat_username=data_chat.get("username", None), token=self.__token)
    #             else:
    #                 raise TogerBadRequest((await response.json()).get("description"))
    #     except aiohttp.ClientError as e:
    #         loggers.event.error(f"ERROR: {e}")

    # async def answer_dice(self, emoji: Optional[str]="🎲", parse_mode: str="HTML", reply_markup=None):
    #     if not isinstance(emoji, str):
    #         # loggers.types.error(f"Expected 'parse_mode' to be a string, got {type(parse_mode).__name__}")
    #         # loggers.types.error("ERROR")
    #         raise ValueError("The 'emoji' parameter cannot be None or not a string.")
    #     if not isinstance(parse_mode, str):
    #         # loggers.types.error("ERROR")
    #         raise ValueError("The 'parse_mode' parameter cannot be None or not a string.")

    #     payload = {
    #         "chat_id": self.__chat_id,
    #         "emoji": emoji,
    #         "parse_mode": parse_mode
    #     }

    #     if reply_markup:
    #         payload["reply_markup"] = reply_markup

    #     try:
    #         async with self.session.post(self.__url + "sendDice", json=payload) as response:
    #             response.raise_for_status()
    #             data = await response.json()
    #             # loggers.types.info("The message has been sent successfully.")
    #             return DiceObject(data.get("result"))
    #     except Exception as e:
    #         loggers.event.error(f"ERROR: {e}")
