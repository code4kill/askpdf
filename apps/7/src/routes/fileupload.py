from flask import Blueprint
from flask_restx import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage

from src.controller.fileupload import upload_file, retrieve_metadata
from src.controller.embedding import generate_embeddings

upload_bp = Blueprint('upload', __name__)

# Updated namespace paths
file_ns = Namespace('files', description='File upload operations')
embedding_ns = Namespace('embeddings', description='Embedding generation operations')
metadata_ns = Namespace('metadata', description='File metadata operations')

# File upload parser
file_upload_parser = reqparse.RequestParser()
file_upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help="PDF file to upload")

# Embedding parser
embedding_parser = reqparse.RequestParser()
embedding_parser.add_argument('file_id', type=str, required=True, help="ID of the uploaded file")

# File upload route
@file_ns.route('/upload')
@file_ns.expect(file_upload_parser)
@file_ns.doc(description="Upload a PDF file to the server")
class FileUpload(Resource):
    def post(self):
        """Handles file uploads"""
        args = file_upload_parser.parse_args()
        file = args['file']
        return upload_file(file)

# Embedding generation route
@embedding_ns.route('/generate_embedding')
@embedding_ns.expect(embedding_parser)
@embedding_ns.doc(description="Generate embeddings from an uploaded PDF file")
class GenerateEmbedding(Resource):
    def post(self):
        """Generates embeddings for the file using file_id"""
        args = embedding_parser.parse_args()
        file_id = args['file_id']
        return generate_embeddings(file_id)

# File metadata retrieval route
@metadata_ns.route('/<string:id>')
@metadata_ns.response(404, 'File not found')
@metadata_ns.param('id', 'The file identifier')
@metadata_ns.doc(description="Retrieve metadata for a specific file")
class FileMetadata(Resource):
    def get(self, id):
        """Get metadata of the file by file ID"""
        metadata = retrieve_metadata(id)
        if not metadata:
            metadata_ns.abort(404, "File not found")
        return metadata
