# config/database.py
import aiomysql
from config import settings

class Database:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if not cls._pool:
            cls._pool = await aiomysql.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASS,
                db=settings.DB_NAME,
                minsize=5,
                maxsize=20,
                autocommit=True
            )
        return cls._pool

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            cls._pool.close()
            await cls._pool.wait_closed()