from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional
from ..config import settings

mongo_client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None
jobs_collection: Optional[AsyncIOMotorCollection] = None


async def connect_to_mongo() -> None:
	global mongo_client, db, jobs_collection
	if mongo_client is None:
		mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
		db = mongo_client[settings.MONGO_DB]
		jobs_collection = db[settings.MONGO_JOBS_COLLECTION]


async def close_mongo_connection() -> None:
	global mongo_client
	if mongo_client:
		mongo_client.close()
		mongo_client = None
















