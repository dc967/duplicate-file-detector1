from pydantic import BaseModel
from typing import List, Optional


class ScanRequest(BaseModel):
    path: str
    recursive: bool = True
    skip_system: bool = True
    hash_method: str = "sha256"
    min_file_size: int = 1024


class DuplicateCopy(BaseModel):
    name: str
    path: str
    size: int
    extension: str
    file_type: str


class DuplicateGroup(BaseModel):
    hash: str
    full_hash: str
    file_type: str
    size: int
    size_formatted: str
    copies: List[DuplicateCopy]
    copies_count: int


class ScanStats(BaseModel):
    total_files: int
    total_duplicates: int
    duplicate_groups: int
    space_recoverable: int
    space_recoverable_formatted: str


class ScanProgress(BaseModel):
    is_scanning: bool
    progress: int
    scanned_files: int
    total_files: int
    current_file: Optional[str] = None


class ScanResponse(BaseModel):
    scan_id: str
    path: str
    status: str
    stats: ScanStats
    duplicates: List[DuplicateGroup]
    scanned_at: str
    completed_at: Optional[str] = None


class ScanHistoryItem(BaseModel):
    scan_id: str
    path: str
    status: str
    total_files: int
    duplicates_found: int
    scanned_at: str
