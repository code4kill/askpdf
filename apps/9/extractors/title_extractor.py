# import fitz

def is_title_case(text):
  """
  Check if the given text is in title case.
  Title case means the first letter of each word is capitalized.
  """
  words = text.split()
  return all(word.istitle() for word in words)

# def extract_title(pdf_path):
#   """
#   Extracts the title of the paper using heuristics based on font size,
#   title case, and position on the first page.
#   """
#   doc = fitz.open(pdf_path)
#   title_candidates = []
#   largest_font_size = 0
  
#   # Load the first page
#   page = doc.load_page(0)  # Only loading the first page

#   # Get the height of the page to determine the mid-point
#   page_height = page.rect.height
#   mid_point = page_height / 2  # Half of the page height

#   # Extract text blocks with font sizes and positions
#   blocks = page.get_text("dict")["blocks"]

#   for block in blocks:
#     for line in block.get("lines", []):
#       for span in line.get("spans", []):
#         text = span.get("text", "").strip()
#         font_size = span.get("size", 0)
#         bbox = span.get("bbox", [])
#         y_pos = bbox[1]  # y-coordinate of the text span

#         # Skip very short text or small font sizes
#         if len(text) <= 5 or font_size < 8:
#           continue

#         # Only consider text that is within the upper half of the page
#         if y_pos > mid_point:
#           continue

#         # Check for title case
#         if not is_title_case(text):
#           continue

#         # Check if this span could be a title candidate
#         if font_size > largest_font_size:
#           largest_font_size = font_size
#           title_candidates = [(text, font_size, y_pos)]  # Track position
#         elif font_size == largest_font_size:
#           title_candidates.append((text, font_size, y_pos))

#   # CSP: Refine title candidate
#   # Sort candidates based on the y-coordinate (should be near the top of the page)
#   title_candidates.sort(key=lambda x: x[2])

#   # Select the first candidate that satisfies reasonable length constraints
#   for candidate in title_candidates:
#     title, font_size, y_pos = candidate
#     word_count = len(title.split())

#     # The title must be in title case and have a reasonable length
#     if 5 <= len(title) and is_title_case(title):
#       return title

#   # Fallback: If no suitable title was found, return a not found message
#   return "Title Not Found"


import fitz  # PyMuPDF

def extract_title(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # First, load the first page
    first_page = doc.load_page(0)
    blocks = first_page.get_text("dict")["blocks"]  # Extract text blocks as dict
    
    # Variables to track the largest font size and corresponding title-case text
    max_font_size = 0
    title = ""

    # Helper function to check if text is in title case
    def is_title_case(text):
        words = text.split()
        return all(word.istitle() for word in words)  # Each word must start with uppercase

    # Iterate over blocks to find the largest font-size text in title case
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    font_size = span["size"]

                    # Check if the text is in title case and has a larger font size
                    if is_title_case(text) and font_size > max_font_size:
                        max_font_size = font_size
                        title = text

    return title

# # Example usage
# pdf_file = "path_to_pdf/your_paper.pdf"
# title = extract_title_case_largest_font(pdf_file)
# print(f"Extracted Title: {title}")

