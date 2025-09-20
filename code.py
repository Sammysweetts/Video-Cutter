import streamlit as st
from moviepy.editor import VideoFileClip
import os
import tempfile

# Set page configuration for a more professional look
st.set_page_config(
    page_title="Streamlit Video Cutter",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def cut_video(input_path, start_time, end_time, output_path):
    """
    Cuts a video file to the specified start and end times.
    """
    try:
        with VideoFileClip(input_path) as video:
            # Ensure the cut times are within the video duration
            if start_time < 0:
                start_time = 0
            if end_time > video.duration:
                end_time = video.duration
            if start_time >= end_time:
                st.error("Error: Start time must be less than end time.")
                return None

            new_clip = video.subclip(start_time, end_time)
            new_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return output_path
    except Exception as e:
        st.error(f"An error occurred during video processing: {e}")
        return None

def main():
    """
    The main function that runs the Streamlit application.
    """
    # --- Sidebar ---
    with st.sidebar:
        st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg", width=200)
        st.title("✂️ Streamlit Video Cutter")
        st.markdown("---")
        st.markdown(
            "This application allows you to upload a video, "
            "select a start and end time, and then cut the video "
            "to the desired length."
        )
        st.markdown("### How to use:")
        st.markdown(
            "1. **Upload your video** using the file uploader.\n"
            "2. **Preview the video** to determine the cut points.\n"
            "3. **Use the sliders** to set the start and end times.\n"
            "4. **Click 'Cut Video'** to process your clip.\n"
            "5. **Preview and download** your finished video!"
        )
        st.markdown("---")
        st.info("Powered by Streamlit and MoviePy")


    # --- Main Application ---
    st.title("Welcome to the Video Cutter App!")
    st.markdown("Upload your video and get cutting in just a few clicks.")

    uploaded_file = st.file_uploader(
        "Choose a video file...", type=["mp4", "mov", "avi", "mkv"]
    )

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            input_video_path = tmp_file.name

        st.video(input_video_path)

        try:
            with VideoFileClip(input_video_path) as video:
                video_duration = video.duration
        except Exception as e:
            st.error(f"Error reading video file: {e}")
            video_duration = 0

        if video_duration > 0:
            st.markdown("### Select Start and End Time")
            start_time, end_time = st.slider(
                "Select a time range to cut (in seconds):",
                0.0,
                video_duration,
                (0.0, video_duration / 2), # Default range
                0.1 # Step size
            )

            st.info(f"Selected range: **{start_time:.1f}s** to **{end_time:.1f}s**")

            if st.button("Cut Video", type="primary"):
                with st.spinner("Processing your video... Please wait."):
                    # Define a temporary output path
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_output:
                        output_video_path = tmp_output.name

                    cut_video_path = cut_video(input_video_path, start_time, end_time, output_video_path)

                    if cut_video_path:
                        st.success("Video has been cut successfully!")
                        st.markdown("### Your Cut Video")
                        st.video(cut_video_path)

                        # Provide a download button
                        with open(cut_video_path, "rb") as file:
                            st.download_button(
                                label="Download Cut Video",
                                data=file,
                                file_name="cut_video.mp4",
                                mime="video/mp4"
                            )

                    # Clean up temporary files
                    os.remove(input_video_path)
                    if cut_video_path:
                        os.remove(cut_video_path)

if __name__ == "__main__":
    main()
