from fastapi import File, UploadFile
from fastapi import APIRouter

from ..core.fileupload import upload_file, retrieve_metadata
from ..utils.embedding import generate_embeddings
from ..schemas import FileResponse, FileMetaData, EmbeddingResponse

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
