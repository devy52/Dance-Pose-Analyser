import streamlit as st
from app.processor import PoseProcessor
from app.logger import logger
from pathlib import Path
import shutil
import cv2
import atexit

# ---------------------------------------------------------
#               FIXED TEMP DIRECTORY + AUTO CLEANUP
# ---------------------------------------------------------
ROOT_TEMP = Path("app/static/temp")
ROOT_TEMP.mkdir(exist_ok=True)

def cleanup_temp():
    """Delete temp folder when the app/process exits."""
    if ROOT_TEMP.exists():
        shutil.rmtree(ROOT_TEMP)
        ROOT_TEMP.mkdir(exist_ok=True)

# Automatically run cleanup when app is closed
atexit.register(cleanup_temp)


# ---------------------------------------------------------
#                  STREAMLIT PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(page_title="Dance Pose Analyser", layout="wide")

st.title("💃 Dance Pose Analyser")
st.markdown("Upload your video to visualize body landmarks and download the processed output.")

uploaded_file = st.file_uploader("🎥 Upload a dance video", type=["mp4", "mov", "avi"])

# Initialize processor
processor = PoseProcessor(mode="VIDEO")


# ---------------------------------------------------------
#               WHEN USER UPLOADS A VIDEO
# ---------------------------------------------------------
if uploaded_file is not None:

    # Save uploaded file to ./temp/
    input_path = ROOT_TEMP / uploaded_file.name
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"📁 File uploaded successfully: **{uploaded_file.name}**")

    # Process Button
    if st.button("🚀 Start Pose Processing"):
        output_path = ROOT_TEMP / f"processed_{uploaded_file.name}"

        with st.spinner("Processing video... please wait."):
            success = processor.process_video(
                input_path=str(input_path),
                output_path=str(output_path)
            )

        if success:
            st.success("✅ Processing complete!")

            # ----------------- Center the processed video -----------------
            st.markdown(
                """
                <div style='text-align:center;'>
                    <h3>🎯 Processed Video Output</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <style>
                .center-video {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .video-wrapper {
                    width: 60%;   /* Medium size */
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<div class='center-video'><div class='video-wrapper'>", unsafe_allow_html=True)
            st.video(str(output_path))
            st.markdown("</div></div>", unsafe_allow_html=True)

            # ----------------- DOWNLOAD + AUTO DELETE -----------------
            with open(output_path, "rb") as f:
                if st.download_button(
                    label="⬇️ Download Processed Video",
                    data=f,
                    file_name=output_path.name,
                    mime="video/mp4"
                ):
                    # Delete both input & output right after download
                    try:
                        if input_path.exists():
                            input_path.unlink()
                        if output_path.exists():
                            output_path.unlink()
                    except Exception as e:
                        logger.error(f"Error deleting temp files: {e}")

        else:
            st.error("❌ Failed to process the video.")

else:
    st.info("📥 Upload a video file to begin.")
