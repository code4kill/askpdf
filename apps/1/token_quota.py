"""
Token and Quota Estimation Module

This module provides functions to estimate the number of tokens
required for processing text and to manage API token quotas.

"""
__author__ = 'mangalbhaskar'

import tiktoken


# ## Estimate the number of tokens in the given text
# def estimate_tokens(text: str) -> int:
#   """
#   Estimates the number of tokens required for the given text.
#   Assumes 1 token per approximately 4 characters.
#   """
#   return len(text) // 4

def estimate_tokens(text: str) -> int:
    """
    Estimates the number of tokens required for the given text using OpenAI's tokenizer.
     cl100k_base is a common tokenizer for GPT-3.5-turbo
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)

## Calculate the remaining quota
def calculate_remaining_quota(used_tokens: int, total_quota: int) -> int:
  """
  Calculates the remaining token quota.
  """
  return total_quota - used_tokens

## Update the number of used tokens after an API call
def update_used_tokens(used_tokens: int, tokens_consumed: int) -> int:
  """
  Updates the used tokens count by adding the tokens consumed in a request.
  """
  return used_tokens + tokens_consumed

## Read and extract text from a PDF file
def read_pdf(file_path: str) -> str:
  """
  Reads a PDF file and extracts the text content.
  """
  from PyPDF2 import PdfReader

  pdf_text = ""
  try:
    pdf_reader = PdfReader(file_path)
    for page in pdf_reader.pages:
      pdf_text += page.extract_text()
  except Exception as e:
    raise RuntimeError(f"Error reading PDF file: {e}")

  return pdf_text
