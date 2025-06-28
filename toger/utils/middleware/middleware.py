from ...exceptions import MiddlewareLimitError
from typing import Callable, Union, Dict
import asyncio


class Middleware:
    """
    Base class for middleware
    """
    def __init__(self):
        self.middlewares = []
    
    def middleware(self):
        def wrapper(func):
            self.middlewares.append(func)
            
            if len(self.middlewares) >= 2:
                raise MiddlewareLimitError("The maximum number of middleware components has been exceeded. Limit: 1.")
            return func
        return wrapper
    
    async def middleware_handle(self, handle, update: dict) -> None:
        if len(self.middlewares) > 0:
            asyncio.create_task(self.middlewares[0](handle, update))
        else:
            await handle(update)