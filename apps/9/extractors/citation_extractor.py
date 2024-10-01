import fitz
import re

def extract_citations(pdf_path):
  citations = []
  reference_found = False

  with fitz.open(pdf_path) as pdf:
    for page_num in range(len(pdf)):
      page = pdf[page_num]
      text = page.get_text("text")
      
      # Look for variations of "References" or "Citations"
      if any(kw in text.lower() for kw in ["references", "citations", "bibliography", "works cited"]):
        reference_found = True
        lines = text.splitlines()

        # Extract citations from the identified reference section
        for line in lines:
          line = line.strip()  # Remove leading and trailing whitespace

          # Check for various citation patterns
          # Pattern 1: Starts with [
          if line.startswith("["):
            citations.append(line)

          # Pattern 2: Author names directly written, e.g., "Smith et al. (2020)"
          elif re.match(r'^[A-Z][a-z]+( et al\.)? \(\d{4}\)', line):
            citations.append(line)

          # Pattern 3: Other common formats, including numeric and text-based citations
          elif re.match(r'^[A-Z].+', line):
            citations.append(line)

          # Additional patterns can be added here based on specific requirements

  # If no citations are found, return a default message
  return citations if citations else ['Citations not found']
