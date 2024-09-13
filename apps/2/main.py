"""
Token and Quota Estimation for PDF - Entry Module

This script is the entry point for estimating the number of tokens
required to process a PDF and managing the API token quota.
It also calculates the estimated cost of using the API.
"""

__author__ = 'mangalbhaskar'

import argparse
import json
import os
from datetime import datetime
from token_quota import estimate_tokens, calculate_remaining_quota, update_used_tokens, read_pdf, calculate_cost

## Quota management
total_quota = 100000  ## Example: total available tokens for the period
used_tokens = 0

def process_pdf(file_path: str, model_key: str, json_path: str = None, conversion_rate: float = 82.0, to_path: str = 'logs'):
  """
  Processes the PDF to estimate token usage, update quota, and calculate cost.
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

  ## Calculate the cost if the JSON file is provided
  cost_data = {}
  if json_path:
    cost_data = calculate_cost(model_key, num_tokens, json_path, conversion_rate)

  ## Generate output JSON data
  output_data = {
    "pdf_file": os.path.basename(file_path),
    "file_path": os.path.abspath(file_path),
    "estimated_tokens": num_tokens,
    "remaining_quota": calculate_remaining_quota(used_tokens, total_quota),
    "cost_estimation": cost_data
  }

  ## Print the output to console
  print(json.dumps(output_data, indent=2))

  ## Ensure the output directory exists
  os.makedirs(to_path, exist_ok=True)

  ## Create the output JSON file
  timestamp = datetime.now().strftime("%d%m%y_%H%M%S")
  output_file = os.path.join(to_path, f"openapi-estimatedcost-{timestamp}.json")
  with open(output_file, 'w') as outfile:
    json.dump(output_data, outfile, indent=2)

  print(f"Output written to {output_file}")

def parse_arguments():
  """
  Parse command-line arguments using argparse.
  """
  parser = argparse.ArgumentParser(description="Token and Quota Estimation for PDF with Cost Calculation")
  parser.add_argument('--from', type=str, dest='from_path', required=True, help='Path to the PDF file to process')
  parser.add_argument('--openapi', type=str, dest='json_path', help='Path to the openapi costing JSON file')
  parser.add_argument('--conversion-rate', type=float, default=82.0, help='USD to INR conversion rate (default: 82.0)')
  parser.add_argument('--to', type=str, dest='to_path', default='logs', help='Directory to save the output JSON file (default: logs)')
  parser.add_argument('--model', type=str, dest='model_key', required=True, help='Model key to use for cost estimation (e.g., gpt-3.5-turbo)')
  return parser.parse_args()

if __name__ == "__main__":
  args = parse_arguments()
  process_pdf(args.from_path, args.model_key, args.json_path, args.conversion_rate, args.to_path)
