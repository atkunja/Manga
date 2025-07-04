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

# 👇 Add this wrapper for Streamlit
def make_video(file_data_list, panel_duration):
    with tempfile.TemporaryDirectory() as tmpdir:
        image_paths = []

        # Save uploaded images to temp files
        for name, file_bytes in file_data_list:
            img_path = os.path.join(tmpdir, name)
            with open(img_path, "wb") as f:
                f.write(file_bytes)
            image_paths.append(img_path)

        # Output video path
        output_path = os.path.join(tmpdir, "output.mp4")

        # Make the video
        success = make_video_from_panels(image_paths, output_path, panel_duration)
        if not success:
            raise Exception("Video generation failed")

        # Read the video back as bytes
        with open(output_path, "rb") as f:
            return f.read()
