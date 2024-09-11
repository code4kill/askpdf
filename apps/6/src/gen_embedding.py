"""Generate emebeddings"""
__author__= "nirajkumar"

import argparse
import json

from datetime import datetime

import tqdm

from .core.common import split_into_chunk
from .core.pdfutils import read_pdf
from .core.openaiutils import generate_embedding
from .token_quota import estimate_tokens, calculate_remaining_quota


def generating_embeddings(text):
  """
  Generate embeddings for the given text
  """
  embeddings = []
  chunks = split_into_chunk(text, chunk_size=500)
  for chunk in chunks:
    embedding = generate_embedding(chunk)
    embeddings.append(embedding)
  return {"chunks": chunks, "embeddings": embeddings}

def save_embeddings(file_path, embeddings, chunks, fileId):
  """
  Save the embeddings to a json file
  """
  data = None
  with open(file_path, 'r') as file:
    data = json.load(file)

  data["files"][fileId] = {
    "chunks": chunks,
    "embeddings": embeddings
  }
  return data


def parse_args():
  parser = argparse.ArgumentParser(description='Generate Embeddings from pdf file.')
  parser.add_argument('--from', dest='from_path', required=True, help='Input PDF file path')
  parser.add_argument('--pdf_path', required=True, help='Input PDF file path')
  args = parser.parse_args()
  return args


def main(args):
  pdf_path = args.pdf_path
  from_path = args.from_path

  text_string = read_pdf(pdf_path)
  estimated = estimate_tokens(text_string)

  print("Estimated tokens: ", f"\033[94m {estimated} \033[0m")
  print("Remaining tokens: ", f"\033[94m {calculate_remaining_quota(estimated, 1000000)} \033[0m")
  print(f" \033[91m Make sure you have enough tokens to process the pdf file !!! \033[0m")

  response = generating_embeddings(text_string)
  fileId = datetime.now().strftime("%Y%m%d_%H%M%S")

  updated_json = save_embeddings(response["embeddings"], response["chunks"], fileId)
  json.dump(updated_json, open(from_path, 'w'))

  print("Embeddings generated and saved to embeddings.json file !!!")
  print("For getting relevant chunks, use the fileId: ", f"\033[93m {fileId} \033[0m")


if __name__ == "__main__":
  args  = parse_args()
  main(args)
