import argparse
from utils import generate_embeddings, split_into_chunk, find_cosine_similarity
import tqdm
import json
from datetime import datetime



def get_relevant_chunk(query, document_id, n=0.8):
  print("qqqq: ",query)
  print("doc",document_id)
  data = None
  query_embedding = generate_embeddings(query)
  with open('embeddings.json', 'r') as file:
    data = json.load(file)
  similarity_scores = find_cosine_similarity(query_embedding, data["files"][document_id]["embeddings"])
  filtered_similarities = [score for score in similarity_scores if score[1] > n]
  index = filtered_similarities[0][0]
  text = data["files"][document_id]["chunks"][index]
  return text


def get_args():
  parser = argparse.ArgumentParser(description="find relevants chunk")
  parser.add_argument("--doc_id", help="document id to search for ")
  parser.add_argument("--query", help="question to ask ?")
  return parser.parse_args()



if __name__ == "__main__":
  args  = get_args()
  chunk_result = get_relevant_chunk(args.query, args.doc_id, 0.8)
  print(chunk_result)