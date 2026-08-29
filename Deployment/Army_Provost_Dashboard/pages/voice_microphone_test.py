
import streamlit as st

st.set_page_config(
    page_title="Voice Microphone Test",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Voice Helpline Microphone Test")

st.write(
    "Use the laptop microphone to record a short "
    "incident report."
)

audio_value = st.audio_input(
    "Record incident report"
)

if audio_value is not None:

    st.success(
        "Audio captured successfully."
    )

    st.audio(
        audio_value,
        format="audio/wav"
    )

    audio_bytes = audio_value.getvalue()

    st.write(
        "Captured audio size:",
        f"{len(audio_bytes):,} bytes"
    )
