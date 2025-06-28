import aiohttp
import ssl
import certifi
import asyncio

ssl_context = ssl.create_default_context(cafile=certifi.where())
session: aiohttp.ClientSession = None

async def start_session():
    global session
    if session is None:
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))
    return session

async def create_session():
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))

async def close_session():
    global session
    if session is not None:
        await session.close()
        session = None
