from typing import Optional, Union, Literal
from datetime import datetime
import asyncio

from ..exceptions import TogerBadRequest
from .. import base
from ..types.from_user import From_user
from ..models import GetUserModel


class GetUser(GetUserModel):
    """
    A class to handle user retrieval from the Toger API.

    This class inherits from GetUserModel and provides functionality to fetch user details
    from the Toger API using the provided authentication string and user ID.

    Args:
        auth_string (Optional[str]): The authentication string for API access.
        user_id (int): The ID of the user to retrieve.

    Methods:
        __call__: Asynchronously calls the API to retrieve user details.

    Raises:
        TogerBadRequest: If the API request fails with an error response.
    """
    
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
                
                
                user_id = data.get("id")
                user_hash = data.get("uh")

                first_name = data.get("first_name")
                username = data.get("username")
                is_bot = data.get("is_bot")
                
                date: datetime = datetime.fromtimestamp(
                    data.get("date", 0) / 1000
                )
                
                return From_user(
                    id=user_id,
                    user_hash=user_hash,
                    
                    first_name=first_name,
                    username=username,
                    is_bot=is_bot,
                    date=date
                )
            else:
                raise TogerBadRequest( (await response.json())["error"]["description"] )