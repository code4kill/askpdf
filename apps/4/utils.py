import os
from dotenv import load_dotenv
from openai import OpenAI
import openai
import numpy as np
import PyPDF2

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_embeddings(text):
  client = OpenAI()
  response = client.embeddings.create(
  model="text-embedding-ada-002",
  input=text,
  encoding_format="float"
  )
  embedding = response.data[0].embedding
  return embedding


def split_into_chunk(text, chunk_size=300):
    words_vocab = text.split()
    chunks = []
    current_chunk = []

    for word in words_vocab:
        current_chunk.append(word)
        if len(current_chunk) == chunk_size:
            chunk = " ".join(current_chunk)
            chunks.append(chunk)
            current_chunk = []  
    if current_chunk:
        chunk = " ".join(current_chunk)
        chunks.append(chunk)

    return chunks

def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    magnitude_of_vector1 = np.linalg.norm(vector1)
    magnitude_of_vector2 = np.linalg.norm(vector2)
    if magnitude_of_vector1 == 0 or magnitude_of_vector2 == 0:
        return 0.0
    cosine_sim = dot_product / (magnitude_of_vector2 * magnitude_of_vector2)
    return cosine_sim

def find_cosine_similarity(vector1, list_of_vectors):
    """Calculate the cosine similarity between a vector and a list of vectors."""
    similarities = []
    for index, vector2 in enumerate(list_of_vectors):
        similarity = cosine_similarity(vector1, vector2)
        similarities.append((index, similarity))
    return similarities

def read_text_from_pdf(path):
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text