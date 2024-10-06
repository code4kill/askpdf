import fitz

def is_title_case(text):
  words = text.split()
  if (len(words) > 0) and words[0].istitle():
    return True
  return False
  
def extract_title(pdf_path):
  doc = fitz.open(pdf_path)
  first_page = doc.load_page(0)
  blocks = first_page.get_text("dict")["blocks"]
  max_font_size = 0
  title = ""
  for block in blocks:
    if "lines" in block:
      for line in block["lines"]:
        for span in line["spans"]:
          text = span["text"].strip()
          font_size = span["size"]
          if is_title_case(text) and font_size > max_font_size:
            max_font_size = font_size
            title = text
  return title

