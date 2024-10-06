import fitz  # PyMuPDF
import re

def extract_tables(page):
    # Get text blocks with their coordinates from the page
    blocks = page.get_text("dict")["blocks"]
    
    # List to hold extracted table rows
    table_data = []
    
    # Iterate through the blocks to detect table-like structures
    for block in blocks:
        if "lines" in block:
            row_data = []
            for line in block["lines"]:
                for span in line["spans"]:
                    # Capture text along with its bounding box (position)
                    row_data.append({
                        "text": span["text"].strip(),
                        "bbox": span["bbox"]
                    })
            # Append the row to the table data
            if row_data:
                table_data.append(row_data)
    
    return table_data

def group_table_by_position(table_data):
    # Group text elements into table rows based on their Y positions
    rows = []
    current_row = []
    current_y = None
    tolerance = 10  # Tolerance for row grouping based on Y position
    
    for row in table_data:
        for cell in row:
            _, y0, _, y1 = cell['bbox']
            middle_y = (y0 + y1) / 2  # Get the vertical center of the cell text
            
            if current_y is None or abs(middle_y - current_y) < tolerance:
                current_row.append(cell["text"])
            else:
                rows.append(current_row)
                current_row = [cell["text"]]
            
            current_y = middle_y
    
    if current_row:
        rows.append(current_row)
    
    return rows

def extract_tables_from_pdf(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # List to hold all extracted tables
    all_tables = []
    
    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        table_data = extract_tables(page)
        if table_data:
            # Group text by their positions to form a structured table
            table = group_table_by_position(table_data)
            all_tables.append({
                "page": page_num + 1,
                "table": table
            })
    
    return all_tables

# # Example usage
# pdf_file = "path_to_pdf/your_document.pdf"
# tables = extract_tables_from_pdf(pdf_file)

# # Output the result
# for table_info in tables:
#     print(f"Page {table_info['page']}:")
#     for row in table_info['table']:
#         print(" | ".join(row))
#     print("\n" + "-" * 50)
