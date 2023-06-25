from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube import capture_screenshots
from openai_whisper import transcribe_audio
from utils import (
    combine_sentence,
    compare_and_delete_images_in_folder,
    rename_files_in_folder,
    extract_link_from_message,
    clear_directory,
)

app = FastAPI()


class MyData(BaseModel):
    link: str
    start: int
    end: int
    annotationLength: int
    articleLength: int


origins = [
    # Replace with your allowed origin(s)
    "https://1ed6-91-193-179-189.eu.ngrok.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    # Replace with your allowed origin(s)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.get("/")
async def get(request: Request):
    return {'Hello! ': 'Welcome to PROFBUH Hackaton API'}


@app.get("/generate")
async def get(request: Request):
    return {'Hello! ': 'Generate Page'}


@app.post("/generate")
async def post(data: MyData):
    
    link = data.link
    start = data.start
    end = data.end
    annotation_length = data.annotationLength
    article_length = data.articleLength

    new_link = extract_link_from_message(link)
    video_title, audio_file, screenshots_dir = capture_screenshots(
        new_link, 'screenshots', 5, start, end)
    compare_and_delete_images_in_folder(screenshots_dir)
    rename_files_in_folder(screenshots_dir)
    srt_file = transcribe_audio(audio_file)
    combine_sentence(screenshots_dir, srt_file, video_title, 
                        'result', annotation_length, article_length)

    file_path = r"result\output.docx"

    response = FileResponse(file_path, filename="downloaded_file.docx",
                            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    clear_directory('screenshots')

    return response

    

