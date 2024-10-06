import os
import json

from src.core.common import split_into_chunk
from src.core.openaiutils import generate_embedding

def generate_embeddings(file_id: str):
    """
    Generate embeddings for the file id
    """
    text = retrieve_text(file_id)
    chunks = split_into_chunk(text)
    embeddings = []
    chunks = split_into_chunk(text, chunk_size=512)
    for chunk in chunks :
        embedding = generate_embedding(chunk)
        embeddings.append(embedding)
    response = {
        "id": file_id,
        "status_code": 200,
        "message": "Embeddings generated successfully",
        "chunks": chunks,
        "embeddings": embeddings
    }
    save_embeddings(file_id, response)    
    return response
  
  
  
def retrieve_text(file_id: str):
    """
    Retrieve text from the file id
    """
    base_path = os.getenv("FILE_UPLOAD_PATH")
    target_file = os.path.join(base_path, file_id + "/extracted_text.txt")
    text = ""
    with open(target_file, "r") as file:
        text = file.read()
    return text

def save_embeddings(file_id: str, embeddings: dict):
    """
    Save embeddings to the file id
    """
    base_path = os.getenv("FILE_UPLOAD_PATH")
    target_file = os.path.join(base_path, file_id + "/embeddings.json")
    with open(target_file, "w") as file:
        json.dump(embeddings, file)
    return True 