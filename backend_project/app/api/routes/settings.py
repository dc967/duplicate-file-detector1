from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/settings", tags=["Settings"])


current_settings = {
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
    return current_settings


@router.post("")
async def save_settings(
    new_settings: dict,
    current_user: dict = Depends(get_current_user)
):
    """Settings save karo"""
    _ = current_user
    current_settings.update(new_settings)
    return {
        "success": True,
        "message": "Settings saved!",
        "settings": current_settings
    }



@router.delete("/history")
async def clear_history(
    current_user: dict = Depends(get_current_user)
):
    """Scan history clear karo"""
    _ = current_user
    from app.api.routes.scan import scan_history
    scan_history.clear()
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
    current_settings.update({
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
    })
    return {
        "success": True,
        "message": "Settings reset!",
        "settings": current_settings
    }



@router.get("/health")
async def settings_health():
    """Health check"""
    return {"status": "ok", "service": "settings"}