import fitz

def extract_sections_with_toc(pdf_path):
  """
  Extract sections and subsections using the Table of Contents (TOC) from the PDF.
  Fallback to heuristic-based section detection if TOC is unavailable.
  """
  doc = fitz.open(pdf_path)
  toc = doc.get_toc()

  sections = []
  
  # If TOC is present, extract sections and subsections
  if toc:
    for entry in toc:
      level, title, page_num = entry
      sections.append({
        "level": level,
        "title": title,
        "page": page_num
      })
  else:
    # If no TOC, apply heuristic extraction based on font sizes or keywords
    sections = heuristic_section_extraction(doc)

  return sections


def heuristic_section_extraction(doc):
  """
  Heuristic-based section extraction if no TOC is present in the PDF.
  This can be customized based on specific patterns in the document.
  """
  sections = []
  for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
      for line in block.get("lines", []):
        for span in line.get("spans", []):
          text = span.get("text", "")
          font_size = span.get("size", 0)

          # Heuristic: Consider large text near the top of the page as potential section titles
          if font_size > 14 and len(text.split()) < 10:
            sections.append({
              "title": text.strip(),
              "page": page_num + 1
            })
  
  return sections
