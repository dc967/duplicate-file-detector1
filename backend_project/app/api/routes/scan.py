from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user
from app.schemas.scan import ScanProgress, ScanRequest, ScanResponse
from app.services.scanner import get_scan_progress, scan_directory
from app.core.database import get_db
from datetime import datetime

router = APIRouter(prefix="/scan", tags=["Scanner"])



@router.post("/start")
async def start_scan(
    request: ScanRequest,
    current_user: dict = Depends(get_current_user),
):
    """Start directory scan and return duplicate results."""
    _ = current_user

    try:
        result = scan_directory(
            path=request.path,
            recursive=request.recursive,
            skip_system=request.skip_system,
            hash_method=request.hash_method,
            min_file_size=request.min_file_size,
        )

        # MongoDB mein save karo
        db = get_db()
        if db is not None:
            await db.scans.insert_one({
                "scan_id": result["scan_id"],
                "path": result["path"],
                "status": result["status"],
                "stats": result["stats"],
                "scanned_at": result["scanned_at"],
                "completed_at": result.get("completed_at"),
                "created_at": datetime.utcnow(),
            })

        return result

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Path not found.",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied for this path.",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scan failed: {exc}",
        )



@router.get("/progress", response_model=ScanProgress)
async def scan_progress(
    current_user: dict = Depends(get_current_user)
):
    """Get current scan progress."""
    _ = current_user
    return ScanProgress(**get_scan_progress())



@router.get("/stats")
async def get_stats(
    current_user: dict = Depends(get_current_user)
):
    """Overall stats do"""
    _ = current_user

    db = get_db()
    if db is None:
        return {
            "total_files": 0,
            "total_duplicates": 0,
            "total_scans": 0,
        }

    # MongoDB se last scan lao
    last_scan = await db.scans.find_one(
        sort=[("created_at", -1)]
    )

    if not last_scan:
        return {
            "total_files": 0,
            "total_duplicates": 0,
            "total_scans": 0,
        }

    total_scans = await db.scans.count_documents({})

    return {
        "total_files": last_scan["stats"]["total_files"],
        "total_duplicates": last_scan["stats"]["total_duplicates"],
        "total_scans": total_scans,
    }



@router.get("/history")
async def get_history(
    current_user: dict = Depends(get_current_user)
):
    """Scan history do"""
    _ = current_user

    db = get_db()
    if db is None:
        return {"history": []}

    # MongoDB se history lao
    cursor = db.scans.find(
        {},
        {"_id": 0}  # _id mat bhejo
    ).sort("created_at", -1).limit(10)

    history = await cursor.to_list(length=10)

    return {"history": history}


@router.get("/health")
async def scan_health():
    """Health check"""
    return {"status": "ok", "service": "scan"}