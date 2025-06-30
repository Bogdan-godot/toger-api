from dataclasses import dataclass


@dataclass
class NewChat:
    title: str
    
    chat_id: int
    link: str