from pydantic import BaseModel
from typing import List


class DeleteFileRequest(BaseModel):
    path: str

class DeleteMultipleRequest(BaseModel):
    paths: List[str]

class MoveToTrashRequest(BaseModel):
    path: str


class DeleteFileResponse(BaseModel):
    success: bool
    message: str
    path: str

class DeleteMultipleResponse(BaseModel):
    success: bool
    message: str
    deleted_count: int
    failed_count: int
    deleted_paths: List[str]
    failed_paths: List[str]
