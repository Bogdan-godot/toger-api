from pydantic import BaseModel

class GetUserModel(BaseModel):
    user_id: int