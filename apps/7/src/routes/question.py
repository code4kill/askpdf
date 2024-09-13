from flask_restx import Namespace, Resource, reqparse
from src.schemas.question_schema import QuestionResponse, QuestionRequest
from src.controller.question_controller import handle_question

question_ns = Namespace('question', description='Question')

@router.get("/history/{id}")
def get_history(id: str):
    """
    Get history of questions
    """
    pass
  
@router.post("/ask", response_model=QuestionResponse)
def ask_question(question_payload:QuestionRequest):
  question_payload = question_payload.dict()
  print(question_payload)
  return handle_question(id=question_payload["id"], question=question_payload["question"])
  
  