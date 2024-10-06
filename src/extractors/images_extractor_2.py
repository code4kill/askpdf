import fitz  # PyMuPDF
import os

def extract_images_and_graphics_from_pdf(pdf_path, output_dir):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image_count = 0
    graphics_data = []
    
    # Iterate through each page of the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract images from the page
        images = page.get_images(full=True)
        for img_idx, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image
            image_filename = f"image_{page_num+1}_{img_idx+1}.{image_ext}"
            image_filepath = os.path.join(output_dir, image_filename)
            with open(image_filepath, "wb") as f:
                f.write(image_bytes)
            
            image_count += 1
            
            # Extract metadata or caption near the image
            caption = extract_caption_near_image(page, img)
            
            # Store image info
            graphics_data.append({
                "type": "image",
                "page": page_num + 1,
                "filename": image_filename,
                "caption": caption
            })
        
        # Extract vector graphics and treat them as figures (if any)
        vectors = extract_vector_graphics(page)
        if vectors:
            vector_filename = f"vector_graphics_page_{page_num+1}.txt"
            vector_filepath = os.path.join(output_dir, vector_filename)
            with open(vector_filepath, "w") as f:
                f.write(vectors)
            
            graphics_data.append({
                "type": "vector",
                "page": page_num + 1,
                "filename": vector_filename,
                "caption": "Possible figure/diagram detected (see extracted vector data)."
            })
    
    return graphics_data

def extract_caption_near_image(page, img):
    # Get image bounding box
    img_x0, img_y0, img_x1, img_y1 = img[6:10]
    
    # Get text blocks near the image
    text_blocks = page.get_text("blocks")
    
    # Look for captions below the image
    caption = ""
    for block in text_blocks:
        block_x0, block_y0, block_x1, block_y1 = block[:4]
        text = block[4].strip()
        
        # Check if the text is close to the image (below it)
        if img_y1 < block_y0 < img_y1 + 50:
            caption += text + " "
    
    return caption.strip()

def extract_vector_graphics(page):
    """
    This function extracts vector graphic data (lines, rectangles, curves)
    from the page. You can customize this to capture and store vector details.
    """
    vector_data = []
    
    # Iterate through the page's drawing instructions
    for item in page.get_drawings():
        if item["type"] == "line":
            vector_data.append(f"Line: start={item['start']}, end={item['end']}")
        elif item["type"] == "rect":
            vector_data.append(f"Rectangle: {item['rect']}")
        elif item["type"] == "curve":
            vector_data.append(f"Curve: {item['points']}")
        # You can handle other types like 'circle', 'bezier', etc.
    
    if vector_data:
        return "\n".join(vector_data)
    else:
        return None

# # Example usage
# pdf_file = "path_to_pdf/your_document.pdf"
# output_directory = "output_graphics"
# graphics = extract_images_and_graphics_from_pdf(pdf_file, output_directory)

# Output extracted data
# for data in graphics:
#     print(f"Page: {data['page']}")
#     print(f"Type: {data['type']}")
#     print(f"File: {data['filename']}")
#     if data['caption']:
#         print(f"Caption: {data['caption']}")
#     print("-" * 40)
