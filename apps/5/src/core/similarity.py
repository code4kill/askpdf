"""similarity matching"""
import numpy as np

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
