import asyncio

from ..utils.token import validate_token
from ..handlers.message import MessageHandler
from .. import base, loggers
from ..methods import (
    GetUpdates, GetMe, GetUser, SendMessage
)
from ..types.from_user import From_user


class Toger:
    def __init__(self, auth_string: str, debug: bool = False):
        validate_token(auth_string)
        
        self.__auth_string = auth_string
        self.debug = debug
        
        self.update_offset = 0
        
        self.__message_handler = MessageHandler(auth_string=self.__auth_string)
        self.message = self.__message_handler
    
    async def __call__(self, call, *args, **kwds):
        if base.session is None:
            await base.start_session()
        
        return await call()
    
    
    async def get_me(self) -> From_user:
        call = GetMe(auth_string=self.__auth_string)
        
        return await self(call)
    
    
    async def get_user(self, user_id: int) -> From_user:
        call = GetUser(
            auth_string=self.__auth_string,
            user_id=user_id
        )
        
        return await self(call)
    
    
    async def send_message(self, chat_id: int, text: str) -> None:
        call = SendMessage(
            auth_string=self.__auth_string,
            chat_id=chat_id,
            
            text=text
        )
        
        return await self(call)
    
    
    async def get_updates(self):
        call = GetUpdates(
            auth_string=self.__auth_string,
            update_offset=self.update_offset,
            
            message_handler=self.__message_handler,
        )
        
        update_id = await self(call)
        
        self.update_offset = update_id
    
    
    async def run(self) -> None:
        try:
            loggers.bot.info("Poll started")
            
            while True:
                try:
                    await asyncio.sleep(1)
                    await self.get_updates()
                except TypeError as e:
                    loggers.bot.error("The Toger API is currently unavailable. A second attempt to receive updates will be made after 5 seconds.")
                    await asyncio.sleep(5)
        finally:
            loggers.bot.info(f"Poll stopped")
            
            await base.session.close()