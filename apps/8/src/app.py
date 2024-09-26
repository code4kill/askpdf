""""
Main file  to run the application.
"""

import argparse
from .parser.meta_parser import extract_pdf_pageno_text, extract_references_section, read_pdf_text, extract_references
from .parser.spacy_parser import extract_named_entity
# from parser import extract_pdf_pageno_text, extract_references_section, read_pdf_text, extract_references, extract_named_entity

def parse_args():
  parser = argparse.ArgumentParser(description='Documents Parser.')
  parser.add_argument('--pdf_path', required=True, help='Input PDF file path')
  args = parser.parse_args()
  return args

def main(args):
  from_path = args['pdf_path']
  first_page = extract_pdf_pageno_text(from_path, 0)
  person = extract_named_entity(first_page)
  text = read_pdf_text(from_path)
  references_sections = extract_references_section(text)
  references = extract_references(references_sections)
  print("References Section :: " ,references_sections)
  print("References :: " ,references)
  print("Named Entity List :: " ,person)


if __name__ == "__main__":
  args  = parse_args()
  main(vars(args))