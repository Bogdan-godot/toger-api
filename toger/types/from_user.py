from datetime import datetime
from dataclasses import dataclass


@dataclass
class From_user:
    id: int
    user_hash: str
    
    first_name: str
    username: str
    
    is_bot: bool
    
    date: datetime
