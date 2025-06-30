from ..transitions import JOIN_TRANSITION
from ..types.new_chat_member import NewChatMember
from ..utils.middleware import Middleware
import asyncio
from datetime import datetime


class ChatMemberHandler(Middleware):
    def __init__(self, auth_string: str):
        self.__auth_string = auth_string
        self.handlers = {}
        
        super().__init__()

    def __call__(self, indicator: str):
        def wrapper(func):
            self.handlers[indicator] = func
            return func
        return wrapper

    def middleware_handle(self, update, indicator: str, me_id: int):
        return super().middleware_handle(self.handle, update, indicator, me_id)

    async def handle(self, update: dict, indicator: str, me_id: int):
        event = update.get("event", {})
        
        type = update.get("type")
        
        chat_id = event.get("chat_id")
        new_member_uid = event.get("user_id")
        # leave_chat_member = message.get("left_chat_member", [])
        
        handler = self.handlers.get(indicator)
        
        if new_member_uid:
            if handler:
                if indicator == JOIN_TRANSITION:
                    if new_member_uid == me_id:
                        return
                    
                    asyncio.create_task(handler(
                        await NewChatMember.create(
                            auth_string=self.__auth_string,
                            type=type,
                            chat_id=chat_id,
                            new_member_uid=new_member_uid
                        )
                    ))
        # elif leave_chat_member:
        #     if indicator == LEAVE_TRANSITION:
        #         if leave_chat_member.get("id") == bot_id:
        #             return
        #         asyncio.create_task(handler(
        #             LeaveChatMember(
        #                 leave_member=leave_chat_member,
        #                 administrator=message.get("from", {}),
        #                 chat=chat,
        #                 message_id=message.get("message_id"),
        #                 token=self.__token,
        #             )
        #         ))