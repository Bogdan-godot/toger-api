from typing import Optional, Union, Literal
from datetime import datetime
import asyncio

from ..exceptions import TogerBadRequest
from .. import base
from ..types.from_user import From_user

class GetMe:
    """
    Handles updates from the Toger API and processes them accordingly.

    This class is responsible for fetching updates from the Toger API, processing them based on their type,
    and handling them through appropriate handlers. It supports both message updates and chat member updates.

    Args:
        auth_string (Optional[str]): Authentication string used for API requests.
        update_offset (Optional[int]): Offset for retrieving updates.
        message_handler (MessageHandler): Handler for processing message updates.
        chat_member_handler (ChatMemberHandler): Handler for processing chat member updates.
        return_data (bool, optional): If True, returns the offset and raw data. Defaults to False.

    Attributes:
        __auth_string (str): Private attribute storing the authentication string.
        __url (str): URL constructed from the auth string for API requests.
        update_offset (int): Current update offset.
        return_data (bool): Flag indicating whether to return raw data.
        __message_handler (MessageHandler): Private attribute for message handling.
        __chat_member_handler (ChatMemberHandler): Private attribute for chat member handling.

    Methods:
        __call__: Asynchronously fetches and processes updates from the API.
        __aenter__: Asynchronous context manager entry point.
        __aexit__: Asynchronous context manager exit point.
    """

    def __init__(self, auth_string: Optional[str]):
        self.__auth_string = auth_string
        self.__url = f"https://toger.org/api/{auth_string}/"
    
    async def __call__(self):
        async with base.session.get(self.__url + "accounts.get") as response:
            if response.ok:
                data = ( await response.json() )[0]
                
                
                user_id = data["id"]
                first_name = data["first_name"]
                username = data["username"]
                is_bot = data["is_bot"]
                
                date: datetime = datetime.fromtimestamp(
                    data.get("date", 0) / 1000
                )
                
                return From_user(
                    user_id,
                    first_name,
                    username,
                    is_bot,
                    date
                )
            else:
                raise TogerBadRequest( (await response.json())["error"]["description"] )