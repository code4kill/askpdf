#!/bin/bash

# Base directory
BASE_DIR="pdf_pipeline"

# Create the base directory and subdirectories
mkdir -p $BASE_DIR/extractors
mkdir -p $BASE_DIR/utils

# Create __init__.py files for package initialization
touch $BASE_DIR/__init__.py
touch $BASE_DIR/extractors/__init__.py
touch $BASE_DIR/utils/__init__.py

# Create main.py with basic template
cat <<EOL > $BASE_DIR/main.py
import os
import argparse
import yaml
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
  title = title_extractor.extract_title(pdf_path, metadata)
  authors = author_extractor.extract_authors(pdf_path, metadata)
  sections = section_extractor.extract_sections(pdf_path)
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
EOL

# Create config.py with basic template
cat <<EOL > $BASE_DIR/config.py
import os

OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'outputs')
EOL

# Create extractors files with basic templates
for extractor in metadata_extractor title_extractor author_extractor section_extractor citation_extractor
do
  cat <<EOL > $BASE_DIR/extractors/$extractor.py
import fitz

def extract_$extractor(pdf_path):
  # Placeholder function for $extractor extraction
  pass
EOL
done

# Create utils/file_handler.py with basic template
cat <<EOL > $BASE_DIR/utils/file_handler.py
import yaml
import os
from config import OUTPUT_DIR

def save_to_yaml(data, filename):
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  output_path = os.path.join(OUTPUT_DIR, filename)
  
  with open(output_path, 'w') as file:
    yaml.dump(data, file, default_flow_style=False)
  print(f"Saved extracted data to {output_path}")
EOL

# Create requirements.txt
cat <<EOL > $BASE_DIR/requirements.txt
pymupdf
pyyaml
EOL

echo "Directory structure and files created successfully!"

