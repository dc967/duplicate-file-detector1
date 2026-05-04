from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# MongoDB Client
client = None
db = None

async def connect_db():
    """MongoDB se connect karo"""
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    print(f" MongoDB Connected: {settings.MONGODB_DB_NAME}")

async def close_db():
    """MongoDB connection close karo"""
    global client
    if client:
        client.close()
        print(" MongoDB Disconnected")

def get_db():
    """Database instance return karo"""
    return db