from pydantic import BaseModel
        
class FileResponse(BaseModel):
    name: str
    id: str
    size: int
    type: str
    status_code: int
    message: str

    class Config:
        from_attributes = False
        
class FileMetaData(BaseModel):
    name: str
    id: str
    size: int
    type: str

    class Config:
        from_attributes = False