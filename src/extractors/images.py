import os
import random
import string

from .pdfutils import getpdf

def extract_images_from_pdf(pdf_path, save_folder):
  doc = getpdf(pdf_path)
  images = []

  for page_number, page in enumerate(doc):
    for img in page.get_images():
      xref = img[0]
      base_image = doc.extract_image(xref)
      image_data = base_image["image"]
      image_format = base_image["ext"]
      image_width = base_image["width"]
      image_height = base_image["height"]
      image_size = len(image_data)

      # Generate a random image name using alphanumeric characters
      random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
      image_path = os.path.join(save_folder, f"{random_name}.{image_format}")
      # with open(image_path, "wb") as f:
      #   f.write(image_data)

      images.append({
        "name": random_name,
        "format": image_format,
        "page_number": page_number + 1,
        "width": image_width,
        "height": image_height,
        "size": image_size
      })

  doc.close()
  return images

