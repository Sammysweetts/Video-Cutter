import streamlit as st
from moviepy.editor import VideoFileClip
import os
from tempfile import NamedTemporaryFile
import time

# ========== Video Cutting Function ==========
def cut_video(input_path, start_time, end_time, output_path):
    try:
        video = VideoFileClip(input_path)
        cut = video.subclip(start_time, end_time)
        cut.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return True, "Video has been cut and saved successfully!"
    except Exception as e:
        return False, str(e)


# ========== Streamlit UI ==========
st.title("🎬 Simple Video Cutter")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)

    start_time = st.number_input("Start time (in seconds)", min_value=0.0, value=0.0, step=0.5)
    end_time = st.number_input("End time (in seconds)", min_value=0.1, value=5.0, step=0.5)

    if st.button("✂️ Cut Video"):
        # Save uploaded video temporarily
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
            temp_input.write(uploaded_file.read())
            input_path = temp_input.name

        # Output path
        output_path = f"cut_video_{int(time.time())}.mp4"

        # Cut video
        with st.spinner("Cutting video..."):
            success, message = cut_video(input_path, start_time, end_time, output_path)

        if success:
            st.success("✅ " + message)

            # Display and download the cut video
            st.video(output_path)

            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="⬇️ Download Cut Video",
                    data=file,
                    file_name="cut_video.mp4",
                    mime="video/mp4"
                )
        else:
            st.error("❌ Error: " + message)
