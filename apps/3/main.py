"""
Chunking and indexing  PDF - Entry Module

This script is used to break the pdf into chunks and indexed based on the contents,
Its uses Thematic and Sliding Window Hybrid technique to create chunks.
"""
__author__ = 'nirajkumar'


from text_utils import text_extractions, QueryBuilder

import argparse
import os

__model_name__ = "all-MiniLM-L6-v2"

def get_args():
  """
  Parse command line arguments.
  """
  parser = argparse.ArgumentParser(description='Tokenize and index PDF.')
  parser.add_argument('--input_pdf', help='Input PDF file path')
  parser.add_argument('--query', help='Question for the pdf document')
  # parser.add_argument('output_dir', help='Output directory path')
  # parser.add_argument('--chunk_size', type=int, default=100, help='Chunk size (default: 100)')
  # parser.add_argument('--window_size', type=int, default=5, help='Window size (default: 5)')
  return parser.parse_args()


if __name__ == '__main__':
  args = get_args()

  # Open the input PDF file
  with open(args.input_pdf, 'rb') as file:
    docs_data = text_extractions(file)
    builder = QueryBuilder()
    builder.create_chunk(docs_data['text'], docs_data['pages'] * 2)
    result = builder.get_answer(args.query)
    print("****************************************************************************************************")
    print(f"Q. {args.query} ? \n\n")
    print("****************************************************************************************************")
    print(f"Answer: \n{result}")