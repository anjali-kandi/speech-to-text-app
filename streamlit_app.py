# streamlit_app.py
import streamlit as st
import tempfile
import os
import whisper
from pydub import AudioSegment
import subprocess

st.set_page_config(page_title="Speech to Text Extractor", layout="wide")
st.title("🎙️ Speech to Text Extractor")

uploaded_file = st.file_uploader("Upload Audio/Video File", type=["mp3", "wav", "m4a", "ogg", "mp4", "avi", "mov", "wmv"])

if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    def convert_to_audio(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.mp3', '.wav', '.m4a', '.ogg']:
            return file_path
        try:
            audio = AudioSegment.from_file(file_path)
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            audio.export(audio_path, format="wav")
            return audio_path
        except:
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            subprocess.run(['ffmpeg', '-i', file_path, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', audio_path])
            return audio_path

    if st.button("🚀 Extract Text"):
        with st.spinner("Processing..."):
            audio_path = convert_to_audio(temp_path)
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            st.success("Transcription complete!")
            st.text_area("📝 Extracted Text", value=result["text"], height=300)
            st.download_button("⬇️ Download Transcript", result["text"], file_name="transcript.txt")
