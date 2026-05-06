from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from app.core.dependencies import get_current_user
from app.schemas.scan import ScanProgress, ScanRequest, ScanResponse
from app.services.scanner import get_scan_progress, scan_directory
from app.services.hash_utils import get_file_type, format_file_size
from app.core.database import get_db
from datetime import datetime
import hashlib
import uuid

router = APIRouter(prefix="/scan", tags=["Scanner"])

scan_history = []

# ─────────────────────────────────────
# Scan Uploaded Files
# ─────────────────────────────────────

@router.post("/upload")
async def scan_uploaded_files(
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Upload karke files scan karo"""
    _ = current_user

    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files uploaded!"
        )

    # Har file ka hash banao
    hash_map = {}

    for file in files:
        try:
            # File content padho
            content = await file.read()

            # Hash banao
            file_hash = hashlib.sha256(content).hexdigest()

            # Extension nikalo
            filename = file.filename or "unknown"
            ext = filename.rsplit(".", 1)[-1].upper() if "." in filename else "FILE"
            file_type = get_file_type(ext.lower())
            size = len(content)

            # Hash map mein add karo
            if file_hash not in hash_map:
                hash_map[file_hash] = []

            hash_map[file_hash].append({
                "name": filename,
                "extension": ext,
                "file_type": file_type,
                "size": size,
                "size_formatted": format_file_size(size),
                "hash": file_hash[:8] + "...",
            })

        except Exception as e:
            continue

    # Duplicates dhundo
    duplicates = []
    total_duplicates = 0
    space_recoverable = 0

    for file_hash, file_list in hash_map.items():
        if len(file_list) > 1:
            copies_count = len(file_list)
            group_size = file_list[0]["size"]

            space_recoverable += group_size * (copies_count - 1)
            total_duplicates += copies_count

            duplicates.append({
                "hash": file_hash[:8] + "...",
                "full_hash": file_hash,
                "file_type": file_list[0]["file_type"],
                "size": group_size,
                "size_formatted": format_file_size(group_size),
                "copies_count": copies_count,
                "copies": file_list,
            })

    # Size ke hisaab se sort karo
    duplicates.sort(key=lambda x: x["size"], reverse=True)

    scan_id = str(uuid.uuid4())[:8]
    result = {
        "scan_id": scan_id,
        "path": "Uploaded Files",
        "status": "completed",
        "stats": {
            "total_files": len(files),
            "total_duplicates": total_duplicates,
            "duplicate_groups": len(duplicates),
            "space_recoverable": space_recoverable,
            "space_recoverable_formatted": format_file_size(space_recoverable),
        },
        "duplicates": duplicates,
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # MongoDB mein save karo
    db = get_db()
    if db is not None:
        await db.scans.insert_one({
            **result,
            "created_at": datetime.utcnow(),
        })

    return result


# ─────────────────────────────────────
# Start Directory Scan
# ─────────────────────────────────────

@router.post("/start")
async def start_scan(
    request: ScanRequest,
    current_user: dict = Depends(get_current_user),
):
    """Start directory scan"""
    _ = current_user

    try:
        result = scan_directory(
            path=request.path,
            recursive=request.recursive,
            skip_system=request.skip_system,
            hash_method=request.hash_method,
            min_file_size=request.min_file_size,
        )

        scan_history.append({
            "scan_id": result["scan_id"],
            "path": result["path"],
            "status": result["status"],
            "total_files": result["stats"]["total_files"],
            "duplicates_found": result["stats"]["total_duplicates"],
            "scanned_at": result["scanned_at"],
        })

        db = get_db()
        if db is not None:
            await db.scans.insert_one({
                **result,
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
            detail="Permission denied.",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scan failed: {exc}",
        )


# ─────────────────────────────────────
# Get Progress
# ─────────────────────────────────────

@router.get("/progress", response_model=ScanProgress)
async def scan_progress(
    current_user: dict = Depends(get_current_user)
):
    _ = current_user
    return ScanProgress(**get_scan_progress())


# ─────────────────────────────────────
# Get Stats
# ─────────────────────────────────────

@router.get("/stats")
async def get_stats(
    current_user: dict = Depends(get_current_user)
):
    _ = current_user

    db = get_db()
    if db is None:
        return {"total_files": 0, "total_duplicates": 0, "total_scans": 0}

    last_scan = await db.scans.find_one(sort=[("created_at", -1)])

    if not last_scan:
        return {"total_files": 0, "total_duplicates": 0, "total_scans": 0}

    total_scans = await db.scans.count_documents({})

    return {
        "total_files": last_scan["stats"]["total_files"],
        "total_duplicates": last_scan["stats"]["total_duplicates"],
        "total_scans": total_scans,
    }


# ─────────────────────────────────────
# Get History
# ─────────────────────────────────────

@router.get("/history")
async def get_history(
    current_user: dict = Depends(get_current_user)
):
    _ = current_user

    db = get_db()
    if db is None:
        return {"history": []}

    cursor = db.scans.find({}, {"_id": 0}).sort("created_at", -1).limit(10)
    history = await cursor.to_list(length=10)

    return {"history": history}


# ─────────────────────────────────────
# Health Check
# ─────────────────────────────────────

@router.get("/health")
async def scan_health():
    return {"status": "ok", "service": "scan"}