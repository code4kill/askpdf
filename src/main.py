## Copyright (c) 2024 mangalbhaskar. All Rights Reserved.
##__author__ = 'mangalbhaskar'
##----------------------------------------------------------
"""
This module extracts metadata, title, authors, sections, citations, images, and tables from a PDF research paper and saves the extracted data in a YAML format.
"""

import os
import logging

from datetime import datetime

from .core import fio
from . import extractors;

## Setup default logs directory
module_name = os.path.splitext(os.path.basename(__file__))[0]
timestamp = datetime.now().strftime("%d%m%y_%H%M%S")
logs_dir = f"logs/{timestamp}"
os.makedirs(logs_dir, exist_ok=True)

## Setup logger
log_filename = f'{logs_dir}/{module_name}.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename)
log = logging.getLogger(__name__)


def parse_arguments():
  """
  Parses command-line arguments for the input PDF file and the output directory.
  """
  import argparse
  parser = argparse.ArgumentParser(description='Extract metadata from a research paper PDF')

  ## Using '--from' for input PDF file and '--to' for output directory
  parser.add_argument('--from', dest='from_path', required=True, help='Path to the PDF file')
  parser.add_argument('--to', dest='to_path', default=logs_dir, help='Output directory path (default: logs/<timestamp>)')

  return parser.parse_args()

def main():
  """
  Main logic to extract metadata and save it in a YAML file.
  """
  args = parse_arguments()
  pdf_path = args.from_path
  output_dir = args.to_path

  log.info(f"Processing PDF: {pdf_path}")
  
  # Extract Metadata
  metadata = extractors.metadata.extract_metadata(pdf_path)
  title = extractors.title.extract_title(pdf_path)
  authors = extractors.author.extract_authors(pdf_path)
  sections = extractors.section.extract_sections_with_toc(pdf_path)
  citations = extractors.citation.extract_citations(pdf_path)
  images = extractors.images.extract_images_from_pdf(pdf_path, output_dir)
  tables = extractors.table.extract_tables_from_pdf(pdf_path)

  extracted_data = {
    'title': title,
    'authors': authors,
    'sections': sections,
    'citations': citations,
    'metadata': metadata,
    'images': images
  }

  # Save to YAML
  filename = os.path.basename(pdf_path).split('.')[0]
  output_filename = f"{output_dir}/{filename}_{timestamp}.yml"

  fio.save_to_yaml(extracted_data, output_filename)

  log.info(f"Data extracted and saved to {output_filename}")
  print(f"Data extracted and saved to {output_filename}")

if __name__ == "__main__":
  main()
