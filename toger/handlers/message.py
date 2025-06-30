from typing import List, LiteralString
from datetime import datetime, timezone
import asyncio
import inspect

from ..types.message import MessageObject
from ..types.command_object import CommandObject
from ..utils.middleware import Middleware


class MessageHandler(Middleware):
    def __init__(self, auth_string: str):
        self.commands = {}
        self.__auth_string = auth_string
        self.default_handler = None
        
        super().__init__()
    
    def __call__(self, command: str = None, commands: List[str] = None, prefix: str = None):
        def wrapper(func):
            if command is None and commands is None:
                self.default_handler = func
            elif command is None and commands:
                for _command in commands:
                    if prefix != None:
                        for i in prefix:
                            _command = i + _command
                            self.commands[_command] = func
            elif isinstance(command, str):
                if prefix != None:
                    for i in prefix:
                        _command = i + command
                        self.commands[_command] = func
                else:
                    _command = command
                    self.commands[_command] = func
            return func
        return wrapper
    
    def middleware_handle(self, update):
        return super().middleware_handle(self.handle, update)
    
    async def handle(self, update):
        event = update.get("event", {})
        text: str = event.get("text", "")
        command = text.split(" ")[0]
        
        
        date: datetime = datetime.fromtimestamp(
            event.get("date", 0) / 1000
        )
        type = event.get("type", None)
        
        handler = self.commands.get(command, self.default_handler)
        
        if handler:
            user_id = event.get("from_id", 0)
            user_hash = event.get("uh")
            
            chat_id: int = event.get("chat_id", 0)
            
            msg_obj = await MessageObject.create(
                auth_string=self.__auth_string,
                
                type=type,
                
                user_id=user_id,
                user_hash=user_hash,
                
                chat_id=chat_id,
                
                message_id=event.get("message_id", 0),
                message_text=text,
                
                date=date
            )
            command_obj = CommandObject(
                text_message=text,
            )
            sig = inspect.signature(handler)
            params = len(sig.parameters)
            if params == 1:
                asyncio.create_task(handler(msg_obj))
            else:
                asyncio.create_task(handler(msg_obj, command_obj))