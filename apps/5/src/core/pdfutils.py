"""pdf utility functions"""
import PyPDF2

## Read and extract text from a PDF file
def read_pdf(file_path: str) -> str:
  """
  Reads a PDF file and extracts the text content.
  """
  pdf_text = ""
  try:
    pdf_reader = PyPDF2.PdfReader(file_path)
    for page in pdf_reader.pages:
      pdf_text += page.extract_text()
  except Exception as e:
    raise RuntimeError(f"Error reading PDF file: {e}")

  return pdf_text

