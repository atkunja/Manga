import streamlit as st
import io
import tempfile
from video_maker import make_video  

st.set_page_config(page_title="📖✨ Manga Animator ✨📖", layout="centered")
st.title("📖✨ Manga Animator ✨📖")
st.caption("Turn your favorite manga chapters into dynamic, anime-style videos!")

st.markdown("Upload images or a ZIP of panels. All processing stays on your machine.")

uploaded_files = st.file_uploader(
    "Upload manga panels (ZIP, JPG, PNG, etc)",
    type=["zip", "jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif", "tif"],
    accept_multiple_files=True
)

panel_duration = st.slider("Panel Duration (seconds)", min_value=0.5, max_value=8.0, value=1.6, step=0.1)

if uploaded_files and st.button("Generate Anime Video!"):
    with st.spinner("Generating animation..."):
        
        file_data = [(f.name, f.getvalue()) for f in uploaded_files]

        try:
            
            video_bytes = make_video(file_data, panel_duration)

            st.success("✨ Done! Download or watch your video below.")
            st.video(video_bytes)

            st.download_button("Download video", video_bytes, file_name="animated_chapter.mp4", mime="video/mp4")
        except Exception as ex:
            st.error(f"Failed to generate video: {ex}")
elif not uploaded_files:
    st.info("Please upload at least one image or a ZIP file to begin.")
