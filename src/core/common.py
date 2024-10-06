"""common utility functions"""
__author__= "nirajkumar"


def split_into_chunk(text:str, chunk_size:int=512):
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
