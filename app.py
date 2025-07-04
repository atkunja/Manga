import streamlit as st
import requests
import io
import tempfile

st.set_page_config(page_title="📖✨ Manga Animator ✨📖", layout="centered")
st.title("📖✨ Manga Animator ✨📖")
st.caption("Turn your favorite manga chapters into dynamic, anime-style videos!")

st.markdown(
    "Upload images or a ZIP of panels. All processing stays on your machine."
)

uploaded_files = st.file_uploader(
    "Upload manga panels (ZIP, JPG, PNG, etc)",
    type=["zip", "jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif", "tif"],
    accept_multiple_files=True
)

panel_duration = st.slider("Panel Duration (seconds)", min_value=0.5, max_value=8.0, value=1.6, step=0.1)

if uploaded_files and st.button("Generate Anime Video!"):
    with st.spinner("Uploading and animating..."):
        files = [("files", (f.name, io.BytesIO(f.getvalue()), f.type)) for f in uploaded_files]
        data = {"panel_duration": str(panel_duration)}
        try:
            r = requests.post("http://localhost:8000/video/", files=files, data=data)
            if r.ok:
                st.success("✨ Done! Download or watch your video below.")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
                    tmpfile.write(r.content)
                    video_path = tmpfile.name
                st.video(video_path)
                with open(video_path, "rb") as v:
                    st.download_button("Download video", v, file_name="animated_chapter.mp4", mime="video/mp4")
            else:
                st.error(f"Error: {r.text}")
        except Exception as ex:
            st.error(f"Failed to contact backend: {ex}")
elif not uploaded_files:
    st.info("Please upload at least one image or a ZIP file to begin.")
