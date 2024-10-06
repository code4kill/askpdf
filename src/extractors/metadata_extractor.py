import fitz

def extract_metadata(pdf_path):
  with fitz.open(pdf_path) as pdf:
    metadata = pdf.metadata
  return {
    'title': metadata.get('title'),
    'author': metadata.get('author'),
    'creation_date': metadata.get('creationDate'),
    'modification_date': metadata.get('modDate'),
    'subject': metadata.get('subject')
  }
