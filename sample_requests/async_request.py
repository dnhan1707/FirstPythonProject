import asyncio
import aiohttp


async def sample_async_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/user/0', headers={}) as response:
            print(response)


asyncio.run(sample_async_request())
