"""
Token and Quota Estimation Module

This module provides functions to estimate the number of tokens
required for processing text, manage API token quotas, and read PDF files.
It also includes functionality to calculate costs based on model pricing.
"""

__author__ = 'mangalbhaskar'

import json
import PyPDF2
import tiktoken # OpenAI's tokenizer

## Estimate the number of tokens in the given text
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
  pdf_text = ""
  try:
    pdf_reader = PyPDF2.PdfReader(file_path)
    for page in pdf_reader.pages:
      pdf_text += page.extract_text()
  except Exception as e:
    raise RuntimeError(f"Error reading PDF file: {e}")

  return pdf_text

## Calculate the estimated cost using the openapi costing JSON file
def calculate_cost(model_key: str, num_tokens: int, json_path: str, conversion_rate: float = 82.0) -> dict:
  """
  Calculate the cost of using the model based on the number of tokens.
  The conversion rate is used to convert the cost from USD to INR.
  """
  try:
    with open(json_path, 'r') as json_file:
      costing_data = json.load(json_file)
      
      if model_key not in costing_data:
        raise ValueError(f"Model '{model_key}' not found in the costing JSON.")
      
      cost_info = costing_data[model_key]
      prompt_cost = cost_info['prompt_cost_per_1k_tokens'] * (num_tokens / 1000)
      completion_cost = cost_info['completion_cost_per_1k_tokens'] * (num_tokens / 1000)
      
      total_cost_usd = prompt_cost + completion_cost
      total_cost_inr = total_cost_usd * conversion_rate
      
      return {
        "model_key": model_key,
        "num_tokens": num_tokens,
        "total_cost_usd": round(total_cost_usd, 4),
        "total_cost_inr": round(total_cost_inr, 4)
      }
  except Exception as e:
    raise RuntimeError(f"Error calculating cost: {e}")
