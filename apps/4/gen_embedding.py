__author__= "nirajkumar"

import argparse
from utils import generate_embeddings, split_into_chunk, read_text_from_pdf
from token_quota import estimate_tokens, calculate_remaining_quota, update_used_tokens, calculate_cost
import tqdm
import json
from datetime import datetime
from config import config



def generating_embeddings(text):
  """
  Generate embeddings for the given text
  """
  embeddings = []
  chunks = split_into_chunk(text, chunk_size=500)
  for chunk in tqdm.tqdm(chunks, desc=f"\033[91m Processing chunks ... \033[0m") :
    embedding = generate_embeddings(chunk)
    embeddings.append(embedding)
  return {"chunks": chunks, "embeddings": embeddings}

def save_embeddings(embeddings, chunks, fileId):
  """
  Save the embeddings to a json file
  """
  file_path = config["storage"]["file_path"]
  data = None
  with open(file_path, 'r') as file:
    data = json.load(file)
  data["files"][fileId] = {
    "chunks": chunks,
    "embeddings": embeddings
  }
  return data

def main(text):
  response = generating_embeddings(text)
  fileId = datetime.now().strftime("%Y%m%d_%H%M%S")
  updated_json = save_embeddings(response["embeddings"], response["chunks"], fileId)
  file_path = config["storage"]["file_path"]
  json.dump(updated_json, open(file_path, 'w'))
  return fileId

def get_args():
  """
  Parse command line arguments.
  return id of documents to extract the relevent chunks
  """
  parser = argparse.ArgumentParser(description='Generate Embeddings from pdf file.')
  parser.add_argument('--pdf_path', help='Input PDF file path')
  return parser.parse_args()



if __name__ == "__main__":
  args  = get_args()
  text_string = read_text_from_pdf(args.pdf_path)
  estimated = estimate_tokens(text_string)
  print("Estimated tokens: ", f"\033[94m {estimated} \033[0m")
  print("Remaining tokens: ", f"\033[94m {calculate_remaining_quota(estimated, 1000000)} \033[0m")
  print(f" \033[91m Make sure you have enough tokens to process the pdf file !!! \033[0m")
  storeId = main(text_string)
  print("Embeddings generated and saved to embeddings.json file !!!")
  print("For getting relevant chunks, use the fileId: ", f"\033[93m {storeId} \033[0m")
  
  