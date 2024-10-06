"""FastAPI Entery points for the application."""
__author__ = 'nirajkumar'


from fastapi import FastAPI
from dotenv import load_dotenv

from .routes import fileupload
from .routes import question

# Load Environment Variables
load_dotenv()
app = FastAPI()

app.include_router(fileupload.router)
app.include_router(question.router)
