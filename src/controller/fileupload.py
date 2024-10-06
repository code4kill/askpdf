import os
from datetime import datetime
import json
from fastapi import File, UploadFile
from src.core.pdfutils import read_pdf_from_file
from src.core.common import write_to_file

def upload_file(file):
    print(file)
    id = datetime.now().strftime("%Y%m%d_%H%M%S")
    response = {
        "name": file.filename,
        "id": "file-" + id,
        "type": file.content_type,
        "status_code": 200,
        "message": f"File uploaded successfully, You can use this {id} id to chat with this document or create embeddings",
    }

    # Define target paths
    target_path = os.getenv("FILE_UPLOAD_PATH", "/tmp")
    file_location = os.path.join(target_path, response['id'])
    dir_name = file_location
    original_file_path = os.path.join(dir_name, file.filename)
    extracted_text_file_path = os.path.join(dir_name, "extracted_text.txt")
    meta_data_file_path = os.path.join(dir_name, "meta_data.json")

    # Create directory and save the file
    os.makedirs(dir_name, exist_ok=True)
    file.save(original_file_path)

    # Calculate the file size after saving
    file_size = os.path.getsize(original_file_path)
    response['size'] = file_size  # Add the file size to the response

    # Read text from the PDF file (you should have a function like this)
    text = read_pdf_from_file(file)

    # Save extracted text and metadata
    write_to_file(extracted_text_file_path, text)
    write_to_file(meta_data_file_path, json.dumps(response))

    # Return the response as JSON
    return json.dumps(response)

def upload_file_from_5(file: UploadFile = File(...)):
    print(file)
    id = datetime.now().strftime("%Y%m%d_%H%M%S")
    response = {
        "name": file.filename,
        "id": "file-" + id,
        "size": file.size,
        "type": file.content_type,
        "status_code": 200,
        "message": f"File uploaded successfully, You can use this {id} id to chat with this documents or create embeddings",
    }
    
    target_path = os.getenv("FILE_UPLOAD_PATH", "/tmp")
    file_location = os.path.join(target_path, response['id'])
    
    # Creating directory for each file to store original file, extracted text, chunks and embeddings.
    dir_name = file_location
    original_file_path = dir_name + "/" + file.filename
    extracted_text_file_path = dir_name + "/" + "extracted_text.txt"
    meta_data_file_path = dir_name + "/" + "meta_data.json"
    
    os.makedirs(dir_name, exist_ok=True)
    # store extracted text 
    text = read_pdf_from_file(file.file)
    write_to_file(extracted_text_file_path, text)
    # store meta data
    write_to_file(meta_data_file_path, json.dumps(response))
    return response

def retrieve_metadata(id: str):
    try:    
        print("id",id)
        base_path = os.getenv("FILE_UPLOAD_PATH", "/tmp")
        meta_data_file_path = os.path.join(base_path, id + "/meta_data.json")
        meta_data = json.load(open(meta_data_file_path, "r"))
        print(meta_data)
    except Exception as e:
        return {
            "name": "",
            "id": "",
            "size": 0,
            "type": "",
            "status_code": 404,
            "message": "File not found"
        }
    
    return meta_data
