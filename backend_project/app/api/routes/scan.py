from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.scan import ScanProgress, ScanRequest, ScanResponse
from app.services.scanner import get_scan_progress, scan_directory

router = APIRouter(prefix="/scan", tags=["Scanner"])


scan_history = []



@router.post("/start", response_model=ScanResponse)
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

       
        scan_history.append({
            "scan_id": result["scan_id"],
            "path": result["path"],
            "status": result["status"],
            "total_files": result["stats"]["total_files"],
            "duplicates_found": result["stats"]["total_duplicates"],
            "scanned_at": result["scanned_at"],
        })

        return ScanResponse(**result)

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

    if not scan_history:
        return {
            "total_files": 0,
            "total_duplicates": 0,
            "total_scans": 0,
        }

    last = scan_history[-1]
    return {
        "total_files": last["total_files"],
        "total_duplicates": last["duplicates_found"],
        "total_scans": len(scan_history),
    }



@router.get("/history")
async def get_history(
    current_user: dict = Depends(get_current_user)
):
    """Scan history do"""
    _ = current_user
    return {"history": scan_history}



@router.get("/health")
async def scan_health():
    """Simple route health check."""
    return {"status": "ok", "service": "scan"}