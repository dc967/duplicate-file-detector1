from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.core.database import get_db

router = APIRouter(prefix="/settings", tags=["Settings"])


DEFAULT_SETTINGS = {
    "hash_method": "sha256",
    "recursive": True,
    "skip_system": True,
    "min_file_size": 1024,
    "move_to_trash": True,
    "auto_scan": False,
    "email_notifications": False,
    "excluded_paths": [
        "/System/Library",
        "/usr/local/bin",
        "/node_modules/**",
    ],
}



@router.get("")
async def get_settings(
    current_user: dict = Depends(get_current_user)
):
    """Settings lao"""
    _ = current_user
    db = get_db()

    if db is None:
        return DEFAULT_SETTINGS

    settings = await db.settings.find_one(
        {"type": "app_settings"},
        {"_id": 0}
    )

    return settings if settings else DEFAULT_SETTINGS



@router.post("")
async def save_settings(
    new_settings: dict,
    current_user: dict = Depends(get_current_user)
):
    """Settings save karo"""
    _ = current_user
    db = get_db()

    if db is not None:
        await db.settings.update_one(
            {"type": "app_settings"},
            {"$set": {**new_settings, "type": "app_settings"}},
            upsert=True
        )

    return {
        "success": True,
        "message": "Settings saved!",
    }



@router.delete("/history")
async def clear_history(
    current_user: dict = Depends(get_current_user)
):
    """Scan history clear karo"""
    _ = current_user
    db = get_db()

    if db is not None:
        await db.scans.delete_many({})

    return {
        "success": True,
        "message": "Scan history cleared!"
    }



@router.post("/reset")
async def reset_settings(
    current_user: dict = Depends(get_current_user)
):
    """Settings reset karo"""
    _ = current_user
    db = get_db()

    if db is not None:
        await db.settings.update_one(
            {"type": "app_settings"},
            {"$set": {**DEFAULT_SETTINGS, "type": "app_settings"}},
            upsert=True
        )

    return {
        "success": True,
        "message": "Settings reset!",
        "settings": DEFAULT_SETTINGS
    }


@router.get("/health")
async def settings_health():
    """Health check"""
    return {"status": "ok", "service": "settings"}