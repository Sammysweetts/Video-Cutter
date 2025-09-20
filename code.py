import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop
import tempfile
import os

st.set_page_config(page_title="🎬 Video Cutter", layout="centered")

# Custom CSS for sleek look
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🎞️ Video Cutter App")
st.caption("Cut your video by choosing start and end times. Powered by Streamlit & MoviePy.")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

# Helper function to convert seconds to hh:mm:ss
def format_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video = VideoFileClip(tfile.name)
    
    st.video(uploaded_file)

    st.markdown("### ✂️ Set Cut Range")
    duration = video.duration
    start_time = st.slider("Start Time", 0.0, duration, 0.0, 0.1)
    end_time = st.slider("End Time", 0.0, duration, duration, 0.1)

    if start_time >= end_time:
        st.warning("⚠️ End time must be greater than Start time.")
    else:
        st.info(f"Selected Range: ⏱️ {format_time(start_time)} to {format_time(end_time)}")

        if st.button("✂️ Cut Video"):
            with st.spinner("Processing..."):
                cut_clip = video.subclip(start_time, end_time)

                output_path = os.path.join(tempfile.gettempdir(), "cut_video.mp4")
                cut_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
                st.success("✅ Video cut successfully!")

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Cut Video",
                        data=f,
                        file_name="cut_video.mp4",
                        mime="video/mp4"
                    )
                
                # Clean up
                cut_clip.close()
                os.remove(output_path)

    # Close video to release file
    video.close()
    os.remove(tfile.name)
