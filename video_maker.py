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
