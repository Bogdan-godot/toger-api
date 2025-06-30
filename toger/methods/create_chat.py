from typing import Optional, Union, Literal
from datetime import datetime
import asyncio

from ..exceptions import TogerBadRequest
from .. import base
from ..models import CreateChatModel
from ..types.new_chat import NewChat


class CreateChat(CreateChatModel):
    """
    A class for creating a chat in Toger API.

    This class inherits from CreateChatModel and provides functionality to create a new chat
    using the Toger API. It requires an authentication string and a title for the chat.

    Args:
        auth_string (Optional[str]): The authentication string for API access.
        title (str): The title of the chat to be created.

    Methods:
        __call__: Asynchronously creates a chat using the provided title and returns a NewChat object.

    Raises:
        TogerBadRequest: If the API request fails.
    """

    def __init__(self, auth_string: Optional[str],
                 title: str):
        super().__init__(title=title)
        
        self.__auth_string = auth_string
        self.__url = f"https://toger.org/api/{auth_string}/"
    
    async def __call__(self):
        async with base.session.get(self.__url + "messages.chatCreate", params={ "title": self.title }) as response:
            if response.ok:
                data = (await response.json()).get("result", {})
                
                chat_id = data.get("chat_id")
                link = data.get("link")
                
                return NewChat(
                    title=self.title,
                    
                    chat_id=chat_id,
                    link=link
                )
            else:
                raise TogerBadRequest(await response.json())