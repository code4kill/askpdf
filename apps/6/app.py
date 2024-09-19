""" API Entery points for the application
"""
__author__ = 'nirajkumar'
__version__ = '0.0.1'


from fastapi import FastAPI
from dotenv import load_dotenv
# from routes import fileupload
from src.routes import fileupload
from src.routes import question

# Load Environment Variables
load_dotenv()
app = FastAPI()

app.include_router(fileupload.router)
app.include_router(question.router)

