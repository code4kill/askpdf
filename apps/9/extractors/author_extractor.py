import fitz
import re

def extract_authors(pdf_path):
  """
  Extracts authors of the paper from the first page.
  Assumes authors are in title case, separated by commas, and may be in bold.
  """
  doc = fitz.open(pdf_path)

  # Load the first page
  page = doc.load_page(0)

  # Extract text blocks with font sizes and properties
  blocks = page.get_text("dict")["blocks"]
  authors_candidates = []

  for block in blocks:
    for line in block.get("lines", []):
      for span in line.get("spans", []):
        text = span.get("text", "").strip()
        
        # Check if the text is long enough and possibly in title case
        if len(text) < 5:
          continue
        
        # Use regex to identify potential author patterns
        if re.match(r'^(?:[A-Z][a-z]+(?: [A-Z][a-z]+)*)(?:, [A-Z][a-z]+(?: [A-Z][a-z]+)*)*$', text):
          authors_candidates.append(text)

  # Deduplicate authors and return them as a list
  authors = list(set(authors_candidates))

  # Return as a comma-separated string
  return ", ".join(authors) if authors else "Authors Not Found"
