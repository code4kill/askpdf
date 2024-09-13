"""
Token and Quota Estimation for PDF - Entry Module

This script is the entry point for estimating the number of tokens
required to process a PDF and managing the API token quota.

"""
__author__ = 'mangalbhaskar'


import argparse
from token_quota import estimate_tokens, calculate_remaining_quota, update_used_tokens, read_pdf

## Quota management
total_quota = 100000  ## Example: total available tokens for the period
used_tokens = 0


def process_pdf(file_path: str):
  """
  Processes the PDF to estimate token usage and update quota.
  """
  global used_tokens  ## To update the global used_tokens

  try:
    ## Read the PDF content
    pdf_text = read_pdf(file_path)
  except RuntimeError as e:
    print(e)
    return

  ## Estimate the number of tokens the text will consume
  num_tokens = estimate_tokens(pdf_text)
  remaining_quota = calculate_remaining_quota(used_tokens, total_quota)

  ## Check if we have enough quota to process the request
  if num_tokens > remaining_quota:
    print(f"Not enough quota. Estimated tokens needed: {num_tokens}, remaining quota: {remaining_quota}.")
    return

  ## Update the used tokens
  tokens_consumed = num_tokens
  used_tokens = update_used_tokens(used_tokens, tokens_consumed)

  print(f"Processed PDF '{file_path}' successfully.")
  print(f"Estimated Tokens: {num_tokens}")
  print(f"Remaining Quota: {remaining_quota - tokens_consumed}")

def parse_arguments():
  """
  Parse command-line arguments using argparse.
  """
  parser = argparse.ArgumentParser(description="Token and Quota Estimation for PDF")
  parser.add_argument('--from', type=str, dest='from_path', required=True, help='Path to the PDF file to process')
  return parser.parse_args()

if __name__ == "__main__":
  args = parse_arguments()
  process_pdf(args.from_path)
