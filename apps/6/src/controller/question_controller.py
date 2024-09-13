import os
import json

from src.core.openaiutils import generate_embedding, qa_prompt_template, chat_completion
from src.core.similarity import find_cosine_similarity


def handle_question(id: str, question: str):
  embedding_json = load_embeddings(id)
  filtered_similarities = find_similar_chunks(question, embedding_json["embeddings"])
  context = ""
  if(len(filtered_similarities) < 1):
    context = "No relevant context found"
  else:
    top_result_index = filtered_similarities[0][0]
    context = embedding_json["chunks"][top_result_index]
  enhanced_prompt = qa_prompt_template(question, context)
  answer = chat_completion(enhanced_prompt, context)
  response = {
    "id": id,
    "status_code": 200,
    "message": "Success",
    "answer": answer
  }
  return response

def load_embeddings(file_id: str):
  base_path = os.getenv("FILE_UPLOAD_PATH", "/tmp")
  embedding_path = os.path.join(base_path, file_id + "/embeddings.json")
  embedding_json = json.load(open(embedding_path, "r"))
  return embedding_json

def find_similar_chunks(question: str, embeddings: list, threshold: float=0.5):
  question_embedding = generate_embedding(question)
  similarity_list = find_cosine_similarity(question_embedding, embeddings)
  filtered_similarities = [score for score in similarity_list if score[1] > threshold]
  return filtered_similarities