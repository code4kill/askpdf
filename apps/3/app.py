import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

## pdf
from PyPDF2 import PdfReader

## openapi
import openai

## tts
from gtts import gTTS
from pydub import AudioSegment

from text_utils import text_extractions


summarise_engine_key = "gpt-3.5-turbo"
openai_api_key = ""

## Create FastAPI app and enable CORS
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Set your OpenAI API key here
openai.api_key = openai_api_key

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF.")

    # Read the PDF content
    pdf_data = text_extractions(file)
    pdf_text = pdf_data.get("text")

    # Estimate tokens (assuming 1 token per ~4 characters)
    metadata = pdf_data.get("metadata")
    no_of_pages = pdf_data.get("pages")
    num_tokens = len(pdf_text) // 4

    # Set a limit for the number of tokens to use with GPT
    max_tokens = 3000
    if num_tokens > max_tokens:
        raise HTTPException(status_code=400, detail="PDF too large for processing.")

    return {"text": pdf_text[:500], "token_estimate": num_tokens}  # Return the first 500 characters as a preview


@app.post("/summarize/")
async def summarize_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF.")

    pdf_data = text_extractions(file)
    pdf_text = pdf_data.get("text")

    # Estimate tokens (assuming 1 token per ~4 characters)
    metadata = pdf_data.get("metadata")
    no_of_pages = pdf_data.get("pages")
    num_tokens = len(pdf_text) // 4
    max_tokens = 3000
    if num_tokens > max_tokens:
        raise HTTPException(status_code=400, detail="PDF too large for processing.")

    # Make the API call to summarize the text
    response = openai.Completion.create(
        engine=summarise_engine_key,
        prompt=f"Summarize the following text:\n\n{pdf_text}",
        max_tokens=150
    )

    summary = response.choices[0].text.strip()
    return {"summary": summary, "token_estimate": num_tokens}


@app.post("/summarize-and-convert/")
async def summarize_and_convert_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF.")

    pdf_data = text_extractions(file)
    pdf_text = pdf_data.get("text")

    # Estimate tokens (assuming 1 token per ~4 characters)
    metadata = pdf_data.get("metadata")
    no_of_pages = pdf_data.get("pages")
    num_tokens = len(pdf_text) // 4
    max_tokens = 3000
    if num_tokens > max_tokens:
        raise HTTPException(status_code=400, detail="PDF too large for processing.")

    response = openai.Completion.create(
        engine=summarise_engine_key,
        prompt=f"Summarize the following text:\n\n{pdf_text}",
        max_tokens=150
    )

    summary = response.choices[0].text.strip()

    # Convert the summary to speech
    tts = gTTS(summary)
    tts.save("summary.mp3")

    # Optionally, convert to a different format if needed
    # sound = AudioSegment.from_mp3("summary.mp3")
    # sound.export("summary.wav", format="wav")

    return {"summary": summary, "mp3_file": "summary.mp3", "token_estimate": num_tokens}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)