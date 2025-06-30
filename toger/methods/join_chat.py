from typing import Optional, Union, Literal
from datetime import datetime
import asyncio

from ..exceptions import TogerBadRequest
from .. import base
from ..models import JoinChatModel
from ..types.new_member import JoinChat


class JoinChat(JoinChatModel):
    """
    A class for joining a chat using a provided authentication string and link.

    This class inherits from JoinChatModel and provides functionality to join a chat by making an API request.
    The authentication string and chat link are used to construct the API URL.

    Args:
        auth_string (Optional[str]): The authentication string for API access.
        link (str): The chat link used to join the chat.

    Attributes:
        __auth_string (Optional[str]): Private attribute to store the authentication string.
        __url (str): Private attribute to store the constructed API URL.

    Methods:
        __call__: Asynchronously joins the chat by making an API request and returns a NewChat object.
                  Raises TogerBadRequest if the request is unsuccessful.
    """

    def __init__(self, auth_string: Optional[str],
                 link: str):
        super().__init__(link=link)
        
        self.__auth_string = auth_string
        self.__url = f"https://toger.org/api/{auth_string}/"
    
    async def __call__(self):
        async with base.session.get(self.__url + "messages.chatJoin", params={ "link": self.link }) as response:
            if response.ok:
                data = (await response.json()).get("result", {})
                
                chat_id = data.get("chat_id")
                
                return JoinChat(
                    chat_id=chat_id
                )
            else:
                raise TogerBadRequest((await response.json()).get("error", "Oops, something went wrong."))