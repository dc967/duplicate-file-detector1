import os
import uuid
from datetime import datetime
from collections import defaultdict
from app.services.hash_utils import (
    get_file_hash,
    get_quick_hash,
    get_file_type,
    format_file_size
)



SYSTEM_PATHS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "/System",
    "/usr",
    "/bin",
    "/sbin",
    "/etc",
]



scan_progress = {
    "is_scanning": False,
    "progress": 0,
    "scanned_files": 0,
    "total_files": 0,
    "current_file": None,
}


def should_skip(path: str, skip_system: bool) -> bool:
    """Kya yeh path skip karni chahiye?"""
    if skip_system:
        for system_path in SYSTEM_PATHS:
            if path.startswith(system_path):
                return True
    return False


def get_all_files(
    directory: str,
    recursive: bool = True,
    skip_system: bool = True,
    min_file_size: int = 1024,
) -> list:
    """Directory se saari files lao"""
    all_files = []

    try:
        if recursive:
            # Saare subfolders bhi scan karo
            for root, dirs, files in os.walk(directory):
                # System paths skip karo
                if should_skip(root, skip_system):
                    continue

                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        # File size check karo
                        size = os.path.getsize(filepath)
                        if size >= min_file_size:
                            all_files.append(filepath)
                    except (OSError, PermissionError):
                        continue
        else:
            # Sirf current folder scan karo
            for file in os.listdir(directory):
                filepath = os.path.join(directory, file)
                if os.path.isfile(filepath):
                    try:
                        size = os.path.getsize(filepath)
                        if size >= min_file_size:
                            all_files.append(filepath)
                    except (OSError, PermissionError):
                        continue

    except (OSError, PermissionError):
        pass

    return all_files




def scan_directory(
    path: str,
    recursive: bool = True,
    skip_system: bool = True,
    hash_method: str = "sha256",
    min_file_size: int = 1024,
) -> dict:
    """Directory scan karo aur duplicates dhundo"""

    global scan_progress

    
    scan_progress.update({
        "is_scanning": True,
        "progress": 0,
        "scanned_files": 0,
        "total_files": 0,
        "current_file": None,
    })

    
    scan_id = str(uuid.uuid4())[:8]
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    all_files = get_all_files(
        directory=path,
        recursive=recursive,
        skip_system=skip_system,
        min_file_size=min_file_size,
    )

    total = len(all_files)
    scan_progress["total_files"] = total

    if total == 0:
        scan_progress["is_scanning"] = False
        return {
            "scan_id": scan_id,
            "path": path,
            "status": "completed",
            "stats": {
                "total_files": 0,
                "total_duplicates": 0,
                "duplicate_groups": 0,
                "space_recoverable": 0,
            },
            "duplicates": [],
            "scanned_at": started_at,
        }

    
    hash_map = defaultdict(list)

    for index, filepath in enumerate(all_files):

        scan_progress.update({
            "scanned_files": index + 1,
            "progress": int(((index + 1) / total) * 100),
            "current_file": os.path.basename(filepath),
        })

        
        quick = get_quick_hash(filepath)
        if quick is None:
            continue

        
        full_hash = get_file_hash(filepath, hash_method)
        if full_hash is None:
            continue


        try:
            size = os.path.getsize(filepath)
            name = os.path.basename(filepath)
            ext = name.rsplit(".", 1)[-1] if "." in name else ""

            hash_map[full_hash].append({
                "name": name,
                "path": filepath,
                "size": size,
                "extension": ext.upper(),
                "file_type": get_file_type(ext),
            })
        except (OSError, PermissionError):
            continue

    
    duplicates = []
    total_duplicates = 0
    space_recoverable = 0

    for file_hash, files in hash_map.items():
        if len(files) > 1:
            # Duplicate group mila!
            group_size = files[0]["size"]
            copies_count = len(files)

            
            space_recoverable += group_size * (copies_count - 1)
            total_duplicates += copies_count

            duplicates.append({
                "hash": file_hash[:8] + "...",
                "full_hash": file_hash,
                "file_type": files[0]["file_type"],
                "size": group_size,
                "size_formatted": format_file_size(group_size),
                "copies_count": copies_count,
                "copies": files,
            })

    
    duplicates.sort(key=lambda x: x["size"], reverse=True)

    
    scan_progress.update({
        "is_scanning": False,
        "progress": 100,
    })

    return {
        "scan_id": scan_id,
        "path": path,
        "status": "completed",
        "stats": {
            "total_files": total,
            "total_duplicates": total_duplicates,
            "duplicate_groups": len(duplicates),
            "space_recoverable": space_recoverable,
            "space_recoverable_formatted": format_file_size(space_recoverable),
        },
        "duplicates": duplicates,
        "scanned_at": started_at,
        "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def get_scan_progress() -> dict:
    """Current scan progress return karo"""
    return scan_progress