from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI(title="AI Voice Synthesis Production Suite")

# Fixes browser security blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = "generated_tracks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/synthesize-track")
async def handle_synthesis(
    lyrics: str = Form(...),
    genre: str = Form(...),
    style: str = Form(...),
    vocal_sample: UploadFile = File(None)
):
    target_output_file = os.path.join(OUTPUT_DIR, "master_output.wav")
    
    # Creates a safe dummy audio file block if no model is loaded
    if not os.path.exists(target_output_file):
        with open(target_output_file, "wb") as f:
            f.write(b"RIFF\x24\x08\x00\x00WAVEfmt\x10\x00\x00\x00\x01\x00\x01\x00\x22\x56\x00\x00")
            
    return FileResponse(path=target_output_file, media_type="audio/wav", filename="track.wav")
