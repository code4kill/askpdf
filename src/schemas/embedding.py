from pydantic import BaseModel
        
class EmbeddingRequest(BaseModel):
    id: str
    
    class Config:
        from_attributes = False
    
    
class EmbeddingResponse(BaseModel):
  id: str
  status_code: int
  message: str
  chunks: list
  embeddings: list

  class Config:
      from_attributes = False