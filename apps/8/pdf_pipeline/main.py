# main.py

import os
import argparse
from datetime import datetime
from extractors import metadata_extractor, title_extractor, author_extractor, section_extractor, citation_extractor
from utils.file_handler import save_to_yaml

def parse_arguments():
  parser = argparse.ArgumentParser(description='Extract metadata from a research paper PDF')
  parser.add_argument('pdf_path', help='Path to the PDF file')
  return parser.parse_args()

def main():
  args = parse_arguments()
  pdf_path = args.pdf_path

  # Extract Metadata
  metadata = metadata_extractor.extract_metadata(pdf_path)
  title = title_extractor.extract_title(pdf_path)  # Enhanced title extraction
  authors = author_extractor.extract_authors(pdf_path)
  sections = section_extractor.extract_sections_with_toc(pdf_path)
  citations = citation_extractor.extract_citations(pdf_path)

  # Combine all extracted info
  extracted_data = {
    'title': title,
    'authors': authors,
    'sections': sections,
    'citations': citations,
    'metadata': metadata
  }

  # Save to YAML
  filename = os.path.basename(pdf_path).split('.')[0]
  timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
  output_filename = f"{filename}_{timestamp}.yml"
  save_to_yaml(extracted_data, output_filename)

if __name__ == "__main__":
  main()
