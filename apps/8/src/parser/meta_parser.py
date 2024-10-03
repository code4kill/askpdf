""""
This module is responsible for parsing the meta data of the pdf file.
"""

import re
import fitz

def extract_pdf_pageno_text(pdf_path, page_no=0):
    """
    Extracts the text of a particular page of the pdf file.

    Args:
        page_no: The page number of the pdf file.
        pdf_path: The path to the pdf file.

    Returns:
        The text of the specified page of the pdf file.
    """
    doc = fitz.open(pdf_path)
    page = doc[page_no]
    text = page.get_text("text")
    return text

def extract_title(text):
  title_pattern = re.compile(r"^[A-Z][\w\s,:-]+$")
  text_line = text.split("\n")
  title = ""
  for line in text_line:
    line = line.strip()
    if re.match(title_pattern, line) and 5 < len(line) < 200:
      title = line
      break
  return title

def extract_references_section(text):
    # Capture the position of the last "References" occurrence, but skip inline citations
    sections = ['conclusion', 'discussion', 'acknowledgments', 'references', 'bibliography']
    last_section_found = None
    for section in sections:
        found_pos = text.lower().rfind(section)
        if found_pos != -1:
            last_section_found = section
            if section in ['references', 'bibliography']:
                break  # Stop at the first occurrence of References or Bibliography

    if last_section_found in ['references', 'bibliography']:
        return text[found_pos:]
    return "References section not found"


def read_pdf_text(pdf_path):
  """
  Reads and returns the text content of a PDF file.

  Args:
    pdf_path: The path to the PDF file.

  Returns:
    The text content of the PDF file.
  """
  doc = fitz.open(pdf_path)
  text = ""
  for page in doc:
    text += page.get_text("text")
  return text



# Function to extract Type 1 references: [1] Author1, Author2. Title. Source, Year.

def extract_type1_references(text):
  pattern = r"\[\d+\]\s([A-Za-z\s,]+)\.\s(.+?)\.\s(.+?,\s\d{4})"
  matches = re.findall(pattern, text)
  references = []

  for match in matches:
      authors = match[0]
      title = match[1]
      publication = match[2]
      references.append({
          'type': 'type1',
          'authors': authors.strip(),
          'title': title.strip(),
          'publication': publication.strip()
      })

  return references

# Function to extract Type 2 references: Author1, Author2, Year. Title. In Conference.
def extract_type2_references(text):
  pattern = r"([A-Za-z\s,]+)\.\s(\d{4})\.\s(.+?)\.\s(In.+|pages.+|arXiv.+)"
  matches = re.findall(pattern, text)
  references = []

  for match in matches:
      authors = match[0]
      year = match[1]
      title_and_source = match[2]
      references.append({
          'type': 'type2',
          'authors': authors.strip(),
          'year': year.strip(),
          'title_and_source': title_and_source.strip()
      })

  return references

# Function to extract Type 3 references: [ARV20] Author1, Author2. Title. Conference/Journal, Year.
def extract_type3_references(text):
  pattern = r"\[([A-Za-z0-9\+\s]+)\]\s([A-Za-z\s,]+)\.\s(.+?)\.\s(.+?,\s\d{4})"
  matches = re.findall(pattern, text)
  references = []

  for match in matches:
      ref_id = match[0]
      authors = match[1]
      title = match[2]
      publication = match[3]
      references.append({
          'type': 'type3',
          'ref_id': ref_id.strip(),
          'authors': authors.strip(),
          'title': title.strip(),
          'publication': publication.strip()
      })

  return references

# Main function to extract references from the text by combining all types
def extract_references(text):
  # Extract each type of references
  type1_references = extract_type1_references(text)
  type2_references = extract_type2_references(text)
  type3_references = extract_type3_references(text)

  # Combine all references into a single list
  all_references = type1_references + type2_references + type3_references

  return all_references

def extract_images_from_pdf(pdf_path):
    # Open the PDF file
  pdf_document = fitz.open(pdf_path)
    
    # List to store all images extracted from the PDF
  extracted_images = []

    # Loop through all the pages in the PDF
  for page_num in range(len(pdf_document)):
    page = pdf_document.load_page(page_num)  # Load a page
    images = page.get_images(full=True)      # Get all images on the page
    
    for img in images:
        # Extract image data
        xref = img[0]  # xref is the image reference number
        image_info = pdf_document.extract_image(xref)
        
        # Append the image data to the extracted_images list
        extracted_images.append({
          "page_num": page_num + 1,         # Page number where the image was found
          "image_data": image_info["image"],# Raw image data (bytes)
          "extension": image_info["ext"],   # Image file extension (e.g., 'png', 'jpeg')
          "width": image_info["width"],     # Image width
          "height": image_info["height"]    # Image height
        })
  
  # Close the PDF document
  pdf_document.close()
  return extracted_images
