""" API Entry points for the application """
__author__ = 'pallawi'
__version__ = '0.0.1'

from flask import Flask
from flask_restx import Api
from src.routes.fileupload import upload_bp, file_ns, embedding_ns, metadata_ns
from src.routes.question import question_ns

app = Flask(__name__)

api = Api(app, version='1.0', title='File Upload API',
          description='A simple API to upload PDF files')

app.register_blueprint(upload_bp, url_prefix='/api')  

api.add_namespace(file_ns)
api.add_namespace(embedding_ns)
api.add_namespace(metadata_ns)
api.add_namespace(question_ns)



if __name__ == '__main__':
    app.run(debug=True)
