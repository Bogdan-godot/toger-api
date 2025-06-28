from pydantic import BaseModel

class SendMessageModel(BaseModel):
    chat_id: int
    text: str