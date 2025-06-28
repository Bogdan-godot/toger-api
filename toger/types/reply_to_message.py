from .from_user import From_user
from .. import loggers, base
from ..exceptions import TogerBadRequest

import aiohttp


class Reply_to_message:
    def __init__(self, full_name: str, user_id: int, message_id: int, username: str, is_bot: bool, language_code: str,
                 token: str, chat_id: int):
        self.__token = token
        self.__url = f"https://toger.org/api/{self.__token}/"
        self.full_name = full_name
        self.user_id = user_id
        self.message_id = message_id
        
        self.__chat_id = chat_id
        
        self.from_user = From_user(fullname=full_name, user_id=user_id, username=username, is_bot=is_bot, language_code=language_code)
        
        self.session = base
    
    async def delete_message(self) -> bool:
        payload = {
            "chat_id": self.__chat_id,
            "message_id": self.message_id,
        }
        try:
            async with self.session.post(self.__url + "deleteMessage", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return True
                else:
                    raise TogerBadRequest((await response.json()).get("description"))
        except Exception as e:
            loggers.event.error(f"{e}")
            return False
    
    async def reply(self, message: str, parse_mode: str="HTML", reply_markup=None):
        if not isinstance(parse_mode, str):
            loggers.event.error(f"Expected 'parse_mode' to be a string, got {type(parse_mode).__name__}")
            return False
        if not isinstance(message, str):
            loggers.event.error(f"Expected 'message' to be a string, got {type(message).__name__}")
            return False
        if message == "" and message == None:
            loggers.event.error("The message is empty.")
            return False
        
        payload = {
            "chat_id": self.__chat_id,
            "text": message,
            "reply_to_message_id": self.message_id,
            "parse_mode": parse_mode
        }

        if reply_markup:
            payload["reply_markup"] = reply_markup

        try:
            async with self.session.post(self.__url + "sendMessage", json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                loggers.event.info("The message has been sent successfully.")
                return True
        except Exception as e:
            loggers.event.error(f"{e}")
            return False
    
    async def reply_photo(self, file_path: str=None, url_photo: str=None, caption: str = None, parse_mode: str="HTML", reply_markup=None):
        if not isinstance(parse_mode, str):
            raise ValueError("The 'parse_mode' parameter cannot be None or not a string.")
        
        if not isinstance(url_photo, str):
            raise ValueError("The 'url_photo' parameter cannot be None or not a string.")
        
        try:
            if file_path:
                with open(file_path, "rb") as photo_file:
                    form_data = aiohttp.FormData()
                    form_data.add_field("chat_id", str(self.__chat_id))
                    form_data.add_field("photo", photo_file, filename=file_path.split("/")[-1])
                    form_data.add_field("parse_mode", parse_mode)
                    form_data.add_field("reply_to_message_id", self.message_id)
            else:
                form_data = aiohttp.FormData()
                form_data.add_field("chat_id", str(self.__chat_id))
                form_data.add_field("photo", url_photo)
                form_data.add_field("parse_mode", parse_mode)
                form_data.add_field("reply_to_message_id", self.message_id)

            if caption:
                form_data.add_field("caption", caption)

            if reply_markup:
                form_data.add_field("reply_markup", reply_markup)
            
            async with self.session.post(f"{self.__url}sendPhoto", data=form_data) as response:
                response.raise_for_status()
                loggers.event.info("The photo was successfully sent.")
                data = await response.json()
                return True
        
        except aiohttp.ClientError as e:
            loggers.event.error(f"ERROR: {e}")
            return False
        
        except FileNotFoundError:
            loggers.event.error(f"ERROR: File not found: {file_path}")
            return False
