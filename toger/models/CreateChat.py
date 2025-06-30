from pydantic import BaseModel

class CreateChatModel(BaseModel):
    title: str