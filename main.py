from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import List
import os
import zipfile
from video_maker import make_video_from_panels

app = FastAPI()

@app.post("/video/")
async def upload(
    files: List[UploadFile] = File(...), 
    panel_duration: float = Form(1.6)
):
    panel_dir = "panels"
    os.makedirs(panel_dir, exist_ok=True)
    # Remove old files
    for f in os.listdir(panel_dir):
        try:
            os.remove(os.path.join(panel_dir, f))
        except Exception:
            pass

    for uploaded in files:
        file_path = os.path.join(panel_dir, uploaded.filename)
        with open(file_path, "wb") as out:
            out.write(await uploaded.read())
        # If ZIP, extract images
        if uploaded.filename.lower().endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zf:
                zf.extractall(panel_dir)
            os.remove(file_path)

    # Gather all images, sorted
    image_files = [
        os.path.join(panel_dir, f)
        for f in sorted(os.listdir(panel_dir))
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif', '.tif'))
    ]

    if not image_files:
        return JSONResponse({"error": "No images found."}, status_code=400)

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "animated_chapter.mp4")
    ok = make_video_from_panels(image_files, output_path, panel_duration)
    if ok:
        return FileResponse(output_path, media_type="video/mp4", filename="animated_chapter.mp4")
    else:
        return JSONResponse({"error": "Video generation failed"}, status_code=500)
