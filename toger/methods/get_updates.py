from typing import Optional, Union, Literal
import asyncio

from ..handlers.message import MessageHandler
from ..handlers.chat_member import ChatMemberHandler
from ..handlers.my_chat_member import MyChatMemberHandler
from .. import loggers, base



class GetUpdates:
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
    
    def __init__(self, auth_string: Optional[str],
                 update_offset: Optional[int],
                 
                 message_handler: MessageHandler,
                 chat_member_handler: ChatMemberHandler,
                 my_chat_member_handler: MyChatMemberHandler,
                 
                 return_data: bool = False
                 ):
        self.__auth_string = auth_string
        self.__url = f"https://toger.org/api/{auth_string}/"

        self.update_offset = update_offset
        self.return_data = return_data

        self.__message_handler: MessageHandler = message_handler
        self.__chat_member_handler: ChatMemberHandler = chat_member_handler
        self.__my_chat_member_handler: MyChatMemberHandler = my_chat_member_handler

    async def __call__(self):
        async with base.session.get(self.__url + "getUpdates", params={"offset": self.update_offset}) as response:
            if response.status == 200:
                data = await response.json()

                if data:
                    for update in data:
                        update_type = update.get("type")
                        
                        if update_type == "message_new":
                            await self.__message_handler.middleware_handle(update)
                            
                            loggers.event.info(
                                "Update has been successfully handled.")
                        elif update_type == "chat_new_member":
                            await self.__chat_member_handler.middleware_handle(update, update_type,
                                                                               self.__auth_string.split(":")[0])
                            await self.__my_chat_member_handler.middleware_handle(update, update_type,
                                                                               self.__auth_string.split(":")[0])
                            
                            loggers.event.info(
                                "Update has been successfully handled.")

                    self.update_offset = data[-1]["update_id"] + 1

                    if self.return_data:
                        return self.update_offset, data
                    return self.update_offset
                else:
                    loggers.event.warning("No updates received.")

                    if self.return_data:
                        return self.update_offset, data
                    return self.update_offset

    async def __aenter__(self):
        return await self()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
