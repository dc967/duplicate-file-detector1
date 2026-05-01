from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



class ScanResult(BaseModel):
    scan_id: str
    path: str
    status: str                   
    total_files: int = 0
    duplicates_found: int = 0
    space_recoverable: int = 0    
    scanned_at: str = ""
    completed_at: Optional[str] = None
    duplicates: list = []