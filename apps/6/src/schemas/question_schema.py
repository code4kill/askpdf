from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
    id: str

    class Config:
        from_attributes = False
        
class QuestionResponse(BaseModel):
    id: str
    status_code: int
    message: str
    answer: str

    class Config:
        from_attributes = False