import streamlit as st
from moviepy.editor import VideoFileClip
from tempfile import NamedTemporaryFile
import os
import time
import re

# ========== Utility Function ==========
def parse_time(timestamp):
    """
    Converts a time string 'HH:MM:SS.MS' or 'MM:SS' or 'SS' to seconds (as float).
    """
    time_parts = re.split(r'[:,]', timestamp)
    time_parts = [float(p) for p in time_parts]

    if len(time_parts) == 1:  # SS
        return time_parts[0]
    elif len(time_parts) == 2:  # MM:SS
        return time_parts[0] * 60 + time_parts[1]
    elif len(time_parts) == 3:  # HH:MM:SS
        return time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2]
    else:
        raise ValueError("Invalid time format. Use HH:MM:SS.MS")

# ========== Video Cutting Function ==========
def cut_video(input_path, start_time, end_time, output_path):
    try:
        video = VideoFileClip(input_path)
        cut = video.subclip(start_time, end_time)
        cut.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return True, "Video cut successfully!"
    except Exception as e:
        return False, str(e)

# ========== Streamlit App ==========
st.set_page_config(page_title="🎬 Advanced Video Cutter", layout="centered")
st.title("🎬 Advanced Video Cutter")
st.markdown("Cut videos with precise time input in **HH:MM:SS.MS** format.")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)

    col1, col2 = st.columns(2)
    with col1:
        start_timestamp = st.text_input("⏱️ Start Time (HH:MM:SS.MS)", value="00:00:00.000")
    with col2:
        end_timestamp = st.text_input("⏱️ End Time (HH:MM:SS.MS)", value="00:00:05.000")

    if st.button("✂️ Cut Video"):
        # Save uploaded video to a temp file
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
            temp_input.write(uploaded_file.read())
            input_path = temp_input.name

        # Create output path
        output_path = f"cut_video_{int(time.time())}.mp4"

        try:
            # Convert HH:MM:SS.MS to seconds
            start_sec = parse_time(start_timestamp.strip())
            end_sec = parse_time(end_timestamp.strip())

            if end_sec <= start_sec:
                st.error("❌ End time must be greater than start time.")
            else:
                with st.spinner("Processing video..."):
                    success, message = cut_video(input_path, start_sec, end_sec, output_path)

                if success:
                    st.success("✅ Video successfully cut!")

                    st.video(output_path)

                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Cut Video",
                            data=f,
                            file_name="cut_video.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("❌ Error cutting video: " + message)

        except ValueError as ve:
            st.error(f"❌ Time Format Error: {ve}")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {e}")
