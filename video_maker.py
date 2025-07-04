import zipfile
import tempfile
import os
import fitz  # PyMuPDF
from moviepy import ImageClip, concatenate_videoclips, vfx

IMAGE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.webp',
    '.bmp', '.tiff', '.gif', '.tif'
)

def make_video_from_panels(image_files, output_path, panel_duration=1.5):
    clips = [
        ImageClip(path)
          .with_duration(panel_duration)
          .with_effects([vfx.Resize(width=800)])
        for path in image_files
    ]
    if not clips:
        return False
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio=False
    )
    return True

def _convert_pdf_to_images(pdf_path, out_folder):
    """Render each page of PDF to a PNG in out_folder."""
    doc = fitz.open(pdf_path)
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(alpha=False)
        img_path = os.path.join(out_folder, f"{base}_page_{i}.png")
        pix.save(img_path)

def make_video(file_data_list, panel_duration):
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1) Write uploads + extract ZIPs
        for name, data in file_data_list:
            p = os.path.join(tmpdir, name)
            with open(p, "wb") as f:
                f.write(data)
            if name.lower().endswith('.zip'):
                with zipfile.ZipFile(p, 'r') as z:
                    z.extractall(tmpdir)

        # 2) First pass: convert ALL PDFs (standalone or in ZIP) to PNGs
        for root, dirs, files in os.walk(tmpdir):
            if "__MACOSX" in dirs:
                dirs.remove("__MACOSX")
            for fn in files:
                if fn.lower().endswith('.pdf'):
                    _convert_pdf_to_images(os.path.join(root, fn), root)

        # 3) Second pass: collect only real images
        image_paths = []
        for root, dirs, files in os.walk(tmpdir):
            if "__MACOSX" in dirs:
                dirs.remove("__MACOSX")
            for fn in sorted(files):
                if fn.startswith('.') or fn.startswith('._'):
                    continue
                if fn.lower().endswith(IMAGE_EXTENSIONS):
                    image_paths.append(os.path.join(root, fn))

        if not image_paths:
            raise Exception("No valid image files found in ZIP or uploads.")

        # 4) Render video
        image_paths.sort()
        out_vid = os.path.join(tmpdir, "output.mp4")
        if not make_video_from_panels(image_paths, out_vid, panel_duration):
            raise Exception("Video generation failed.")

        # 5) Return bytes
        with open(out_vid, "rb") as f:
            return f.read()
