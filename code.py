import streamlit as st
import os
from moviepy.editor import VideoFileClip
from pathlib import Path
import tempfile

st.set_page_config(page_title="🎬 Advanced Video Cutter", layout="centered")

st.title("🎬 Ultra-Advanced Video Cutter with Audio Preservation")
st.markdown("Cut any video without losing audio quality - right here in your browser!")

# Temporary file saving directory
TEMP_DIR = tempfile.gettempdir()

# Upload video file
video_file = st.file_uploader("📤 Upload your video file:", type=["mp4", "mov", "avi", "mkv"])

def convert_to_seconds(hh, mm, ss):
    """Convert hh:mm:ss to seconds"""
    return int(hh)*3600 + int(mm)*60 + float(ss)

def cut_video(input_path, start_time, end_time, output_path):
    try:
        video = VideoFileClip(input_path)
        if end_time > video.duration:
            st.error(f"❌ End time can't be greater than the total video duration: {video.duration:.2f}s")
            return False, None
        cut = video.subclip(start_time, end_time)
        cut.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return True, output_path
    except Exception as e:
        st.error(f"❌ Error processing video: {e}")
        return False, None


if video_file:
    # Save uploaded video temporarily
    input_path = os.path.join(TEMP_DIR, video_file.name)
    with open(input_path, "wb") as f:
        f.write(video_file.read())

    video = VideoFileClip(input_path)
    duration = video.duration
    st.video(video_file, format="video/mp4")

    st.markdown(f"ℹ️ **Video Duration**: `{duration:.2f}` seconds")

    st.subheader("✂️ Set Cut Points (in seconds)")
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.number_input("Start Time (seconds):", min_value=0.0, max_value=float(duration - 1), value=0.0, step=0.5)
    with col2:
        end_time = st.number_input("End Time (seconds):", min_value=0.1, max_value=float(duration), value=min(5.0, duration), step=0.5)

    if start_time >= end_time:
        st.warning("⚠️ End time must be greater than start time.")

    output_filename = Path(video_file.name).stem + f"_CUT_{int(start_time)}_{int(end_time)}.mp4"
    output_path = os.path.join(TEMP_DIR, output_filename)

    if st.button("✂️ Cut Video"):
        with st.spinner("Cutting video... please wait ⏳"):
            success, path = cut_video(input_path, start_time, end_time, output_path)
            if success:
                st.success("✅ Video cut successfully!")
                st.video(path)
                with open(path, "rb") as out_file:
                    st.download_button(label="📥 Download Cut Video", data=out_file, file_name=output_filename, mime="video/mp4")
