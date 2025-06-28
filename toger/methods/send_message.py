from typing import Optional, Union, Literal
from datetime import datetime
import asyncio

from ..exceptions import TogerBadRequest, ValidationError
from .. import base, loggers
from ..types.from_user import From_user
from ..models import SendMessageModel

class SendMessage(SendMessageModel):
    def __init__(self, auth_string: Optional[str],
                 chat_id: int,
                 text: str):
        super().__init__(
            chat_id=chat_id,
            text=text
        )
        if self.text == "" and self.text == None:
            raise ValidationError("The message is empty.")
        
        self.__auth_string = auth_string
        self.__url = f"https://toger.org/api/{auth_string}/"
        
    async def __call__(self):    
        payload = {
            "chat_id": self.chat_id,
            
            "text": self.text
        }
        
        async with base.session.get(self.__url + "messages.send", params=payload) as response:
            if not response.ok:
                raise TogerBadRequest(await response.json())
            
            data = await response.json()
            
            loggers.event.info("The message has been sent successfully.")
            return data["result"]["message_id"]