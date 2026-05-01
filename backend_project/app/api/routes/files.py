import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user
from app.schemas.file import (
    DeleteFileRequest,
    DeleteFileResponse,
    DeleteMultipleRequest,
    DeleteMultipleResponse,
    MoveToTrashRequest,
)

router = APIRouter(prefix="/file", tags=["Files"])


@router.delete("", response_model=DeleteFileResponse)
async def delete_file(
    request: DeleteFileRequest,
    current_user: dict = Depends(get_current_user),
):
    """Single file delete karo"""
    _ = current_user

    
    if not os.path.exists(request.path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {request.path}"
        )

    
    if not os.path.isfile(request.path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path is not a file!"
        )

    try:
        os.remove(request.path)
        return DeleteFileResponse(
            success=True,
            message="File deleted successfully!",
            path=request.path
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied!"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {e}"
        )


@router.delete("/multiple", response_model=DeleteMultipleResponse)
async def delete_multiple_files(
    request: DeleteMultipleRequest,
    current_user: dict = Depends(get_current_user),
):
    """MULTIPLE FILES DELETE KARO"""
    _  = current_user

    deleted_paths = []
    failed_paths = []

    for path in request.paths:
        try:
            if os.path.exists(path) and os.path.isfile(path):
                os.remove(path)
                deleted_paths.append(path)
            else:
                failed_paths.append(path)
        except Exception:
            failed_paths.append(path)

    return DeleteMultipleResponse(
        success=len(deleted_paths) > 0,
        message=f"{len(deleted_paths)} files deleted!",
        deleted_count=len(deleted_paths),
        failed_count=len(failed_paths),
        deleted_paths=deleted_paths,
        failed_paths=failed_paths,
    )



@router.post("/trash", response_model=DeleteFileResponse)
async def move_to_trash(
    request: MoveToTrashRequest,
    current_user: dict = Depends(get_current_user),
):
    """File trash mein bhejo"""
    _ = current_user

    
    if not os.path.exists(request.path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {request.path}"
        )

    try:
        
        trash_dir = os.path.join(os.path.expanduser("~"), ".dupliscan_trash")
        os.makedirs(trash_dir, exist_ok=True)

       
        filename = os.path.basename(request.path)
        trash_path = os.path.join(trash_dir, filename)

        shutil.move(request.path, trash_path)

        return DeleteFileResponse(
            success=True,
            message=f"File moved to trash!",
            path=request.path
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied!"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Move to trash failed: {e}"
        )



@router.get("/health")
async def files_health():
    """Health check"""
    return {"status": "ok", "service": "files"}