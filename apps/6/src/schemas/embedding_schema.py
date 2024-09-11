from pydantic import BaseModel
        
class EmbeddingRequest(BaseModel):
    id: str
    
    class Config:
        orm_mode = False
    
    
class EmbeddingResponse(BaseModel):
  id: str
  status_code: int
  message: str
  chunks: list
  embeddings: list

  class Config:
      orm_mode = False