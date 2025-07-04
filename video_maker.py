import zipfile
import tempfile
import os
from moviepy import ImageClip, concatenate_videoclips, vfx

def make_video_from_panels(image_files, output_path, panel_duration=1.5):
    clips = []
    for img_path in image_files:
        clip = (
            ImageClip(img_path)
            .with_duration(panel_duration)
            .with_effects([vfx.Resize(width=800)])
        )
        clips.append(clip)
    if not clips:
        return False
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=24, codec="libx264", audio=False)
    return True

def make_video(file_data_list, panel_duration):
    with tempfile.TemporaryDirectory() as tmpdir:
        image_paths = []

        for name, file_bytes in file_data_list:
            file_path = os.path.join(tmpdir, name)
            with open(file_path, "wb") as f:
                f.write(file_bytes)

            if name.lower().endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdir)
                
                # 🔍 Walk through extracted folder structure to find images
                for root, _, files in os.walk(tmpdir):
                    for fname in sorted(files):
                        if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.gif')):
                            image_paths.append(os.path.join(root, fname))
            elif name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.gif')):
                image_paths.append(file_path)

        if not image_paths:
            raise Exception("No valid image files found.")

        output_path = os.path.join(tmpdir, "output.mp4")
        success = make_video_from_panels(image_paths, output_path, panel_duration)
        if not success:
            raise Exception("Video generation failed")

        with open(output_path, "rb") as f:
            return f.read()
