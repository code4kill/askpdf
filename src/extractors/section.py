from collections import Counter

from .pdfutils import getpdf

def extract_sections_with_toc(pdf_path):
  """
  Extract sections and subsections using the Table of Contents (TOC) from the PDF.
  Fallback to heuristic-based section detection if TOC is unavailable.
  Content for each section is also extracted.
  """
  doc = getpdf(pdf_path)
  toc = doc.get_toc()

  sections = []

  # If TOC is present, extract sections, subsections, and content
  if toc:
    for i, entry in enumerate(toc):
      level, title, start_page = entry
      
      # Ensure the page numbers are within the document range
      start_page = max(1, min(start_page, len(doc))) - 1  # Convert to zero-indexed

      # Determine the end page of the section
      if i < len(toc) - 1:
        _, _, next_start_page = toc[i + 1]
        end_page = max(1, min(next_start_page - 1, len(doc))) - 1  # Convert to zero-indexed
      else:
        end_page = len(doc) - 1  # Last section goes till the last page

      # Extract content from the section start to the section end
      section_content = ""
      for page_num in range(start_page, end_page + 1):
        page = doc.load_page(page_num)
        
        # Try different text extraction modes
        text = page.get_text("text")  # Plain text mode
        if not text.strip():  # Fallback to block mode if plain text is empty
          text = page.get_text("blocks")
          text = " ".join([block[4] for block in text])  # Extract text from blocks
        
        section_content += text + "\n"

      sections.append({
        "title": title,
        "page": start_page + 1,  # Convert back to one-indexed for user clarity
        "content": section_content.strip()
      })
  
  # If no TOC is present, apply heuristic extraction based on font sizes or keywords
  else:
    sections = heuristic_section_extraction(doc)

  return sections

def get_common_font_sizes(doc):
  """
  Analyze the document to get a distribution of font sizes.
  Returns a list of font sizes sorted by frequency.
  """
  font_sizes = []

  # Iterate through each page in the document
  for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
      for line in block.get("lines", []):
        for span in line.get("spans", []):
          font_sizes.append(span.get("size", 0))

  # Count the frequency of each font size
  font_size_counts = Counter(font_sizes)
  
  # Sort the font sizes by frequency in descending order
  sorted_font_sizes = sorted(font_size_counts.items(), key=lambda x: x[1], reverse=True)
  
  return sorted_font_sizes

def heuristic_section_extraction(doc):
  """
  Heuristic-based section extraction with dynamic font size detection.
  This extracts both section titles and their content based on the most frequent font sizes.
  """
  sections = []
  current_section = None
  
  # Get common font sizes to infer section headers
  sorted_font_sizes = get_common_font_sizes(doc)
  if not sorted_font_sizes:
    return sections
  
  # Assume the most common font size is body text
  body_font_size = sorted_font_sizes[0][0]
  
  # Use all larger font sizes as potential section titles
  header_font_sizes = [size for size, _ in sorted_font_sizes if size > body_font_size]

  # Iterate through each page in the document
  for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
      for line in block.get("lines", []):
        for span in line.get("spans", []):
          text = span.get("text", "").strip()
          font_size = span.get("size", 0)

          # Detect section titles based on header font sizes
          if font_size in header_font_sizes and len(text.split()) < 15 and (
              text[0].isdigit() or text.istitle()):
            
            # Close the previous section
            if current_section:
              sections.append(current_section)

            # Start a new section
            current_section = {
              "title": text,
              "page": page_num + 1,
              "content": ""  # Initialize empty content for the section
            }
          elif current_section:
            # Accumulate content for the current section
            current_section["content"] += text + " "

    # If there's an active section after processing the page, append it
    if current_section:
      sections.append(current_section)
      current_section = None  # Reset for the next page

  return sections
