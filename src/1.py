"""GenAI Namaste World!
"""
__author__ = 'nirajkumar'


import argparse
import json

from datetime import datetime

import tqdm

from .core.openaiutils import generate_embedding, chat_completion
from .core.similarity import find_cosine_similarity


def get_relevant_chunk(data, query, doc_id, threshold=0.5):
  # print(f'data:: {data}')
  print(f'query:: {query}')
  print(f'doc_id:: {doc_id}')
  embeddings = data["files"][doc_id]["embeddings"]
  # print(f'embeddings:: {embeddings}')
  print(f'threshold:: {threshold}')
  query_embedding = generate_embedding(query)
  print(f'query_embedding:: {query_embedding}')

  similarity_scores = find_cosine_similarity(query_embedding, embeddings)
  filtered_similarities = [score for score in similarity_scores if score[1] > threshold]
  text = 'No response'
  if filtered_similarities:
    index = filtered_similarities[0][0]
    text = data["files"][doc_id]["chunks"][index]
  return text


def parse_args():
  parser = argparse.ArgumentParser(description="find relevant chunk")
  parser.add_argument("--query", required=True, help="question to ask?")
  parser.add_argument("--doc_id", required=True, help="document id to search for")
  parser.add_argument('--from', dest='from_path', required=True, help='Input embedding file')
  args = parser.parse_args()
  return args

def retrieve_answer(data, query, doc_id, threshold=0.5):
  chunk_result = get_relevant_chunk(data, query, doc_id, threshold)
  answer = chat_completion(query, chunk_result)
  return answer

def main(args):
  query = args['query']
  doc_id = args['doc_id']
  from_path = args['from_path']

  print(f"\033[91m Your question regarding to document id \033[0m {doc_id} is : \n \033[94m {query} \033[0m \n")

  with open(from_path, 'r') as file:
    data = json.load(file)

  answer = retrieve_answer(data, query, doc_id)
  print(f"Your answer is : \n \033[92m {answer} \033[0m \n")

if __name__ == "__main__":
  args  = parse_args()
  main(vars(args))
