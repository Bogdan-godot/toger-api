from typing import Optional, Union, Literal
import asyncio

from ..handlers.message import MessageHandler
from .. import loggers, base


class GetUpdates:
    """
    Get updates method
    Source: core.Toger.org/bots/api#getupdates #временно
    """
    def __init__(self, auth_string: Optional[str],
                 update_offset: Optional[int],
                 message_handler,
                 ):
        self.__auth_string = auth_string
        self.__url = f"https://toger.org/api/{auth_string}/"
        
        self.update_offset = update_offset
        
        self.__message_handler: MessageHandler = message_handler
    
    async def __call__(self):
        async with base.session.get(self.__url + "getUpdates", params={"offset": self.update_offset}) as response:
            if response.status == 200:
                data = await response.json()
                
                if data:
                    for update in data:
                        update_type = update.get("type")
                        if update_type == "message_new":
                            loggers.event.info("Update has been successfully handled.")
                            await self.__message_handler.middleware_handle(update)

                    self.update_offset = data[-1]["update_id"] + 1
                    return self.update_offset
                else:
                    loggers.event.warning("No updates received.")
                    return self.update_offset
    
    async def __aenter__(self):
        return await self()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass