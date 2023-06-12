from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
import os

from conf.config import config

mongo_config = config.mongo

mongo_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    global mongo_client
    try:
        if not mongo_client:
            mongo_client = AsyncIOMotorClient(
                f"mongodb://{mongo_config.username}:{mongo_config.password}@{mongo_config.host}:{mongo_config.port}")
            logger.info("Connected to mongo")
    except Exception as err:
        logger.error(f"Failed to connect mongo: {err}")
        os._exit(1)


async def close_mongo_connection():
    global mongo_client
    if mongo_client:
        logger.info("Closing mongo connection...")
        mongo_client.close()
        mongo_client = None
        logger.info("Closed mongo connection")


def get_db():
    global mongo_client
    if not mongo_client:
        connect_to_mongo()

    return mongo_client[mongo_config.db_name]
