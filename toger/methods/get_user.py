from typing import Optional, Union, Literal
from datetime import datetime
import asyncio

from ..exceptions import TogerBadRequest
from .. import base
from ..types.from_user import From_user
from ..models import GetUserModel

class GetUser(GetUserModel):
    def __init__(self, auth_string: Optional[str],
                 user_id: int):
        super().__init__(
            user_id=user_id
        )
        
        self.__auth_string = auth_string
        self.__url = f"https://toger.org/api/{auth_string}/"
    
    async def __call__(self):
        async with base.session.get(self.__url + "accounts.get", params={"user_ids": self.user_id}) as response:
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