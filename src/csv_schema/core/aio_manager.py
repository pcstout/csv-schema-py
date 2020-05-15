import asyncio


class AioManager:

    @classmethod
    def start(cls, func, **kwargs):
        return asyncio.run(cls._start_async(func, **kwargs))

    @classmethod
    async def _start_async(cls, func, **kwargs):
        return await func(**kwargs)
