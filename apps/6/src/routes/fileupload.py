from fastapi import File, UploadFile
from fastapi import APIRouter

from src.schemas.file import FileResponse, FileMetaData
from src.schemas.embedding_schema import EmbeddingResponse
from src.controller.fileupload import upload_file, retrieve_metadata
from src.controller.embedding import generate_embeddings

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/upload", response_model=FileResponse)
def file_upload(file: UploadFile = File(...)):
    return upload_file(file)

@router.post("/generate_embedding", response_model=EmbeddingResponse)
def call_generate_embeddings(id):
    return generate_embeddings(id)

@router.get("/metadata/{id}", response_model=FileMetaData)
def get_metadata(id: str):
    """
    Get metadata of the file
    """
    return retrieve_metadata(id)
    