from .pdfutils import getpdf

def extract_metadata(pdf_path):
  with getpdf(pdf_path) as pdf:
    metadata = pdf.metadata
  return {
    'title': metadata.get('title'),
    'author': metadata.get('author'),
    'creation_date': metadata.get('creationDate'),
    'modification_date': metadata.get('modDate'),
    'subject': metadata.get('subject')
  }
