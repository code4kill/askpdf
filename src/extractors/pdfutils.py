"""pdf utility functions"""

## Read and extract text from a PDF file
def read_pdf(file_path: str) -> str:
  import PyPDF2

  """Reads a PDF file and extracts the text content."""
  pdf_text = ""
  try:
    pdf_reader = PyPDF2.PdfReader(file_path)
    for page in pdf_reader.pages:
      pdf_text += page.extract_text()
  except Exception as e:
    raise RuntimeError(f"Error reading PDF file: {e}")

  return pdf_text

def read_pdf_from_file(file):
  import PyPDF2

  """Reads a PDF file and extracts the text content."""
  pdf_text = ""
  try:
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
      pdf_text += page.extract_text()
  except Exception as e:
    raise RuntimeError(f"Error reading PDF file: {e}")

  return pdf_text

def getpdf(file_path: str):
  import fitz  # PyMuPDF
  """get pdf object using pymupdf library."""
  pdf_reader = ""
  try:
    pdf_reader = fitz.open(file_path)
  except Exception as e:
    raise RuntimeError(f"Error reading PDF file: {e}")
  return pdf_reader
