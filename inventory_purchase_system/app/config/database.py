from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config.settings import settings


async def connect_to_mongodb():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    from app.models.supplier_model import Supplier
    from app.models.item_model import Item
    from app.models.purchase_model import Purchase
    from app.models.user_model import User

    await init_beanie(database=db, document_models=[Supplier, Item, Purchase, User])
    print(f"[DB] Connected → {settings.DATABASE_NAME}")


async def disconnect_from_mongodb():
    print("[DB] Disconnected")
