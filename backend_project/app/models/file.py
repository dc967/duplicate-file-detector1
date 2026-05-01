from pydantic import BaseModel

class File(BaseModel):
    name: str
    path: str
    size: int
    extension: str
    hash: str
    file_type: str