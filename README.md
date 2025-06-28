## Установка
```bash
pip install git+https://github.com/Bogdan-godot/toger-api.git
```

### В данный момент библиотека toger не имеет документации, но не смотря на это мы дадим вам пример кода на ней
```python
import asyncio
import logging

from toger import Toger
from toger.types import MessageObject, CommandObject

bot = Toger("{ID}:{TOKEN}")

logging.basicConfig(level=logging.INFO)


@bot.message.middleware()
async def middleware(handler, call: dict):
    return await handler(call)


@bot.message("print")
async def start(msg: MessageObject, command: CommandObject):
    await msg.answer(command.args)


if __name__ == "__main__":
    asyncio.run(bot.run())
```