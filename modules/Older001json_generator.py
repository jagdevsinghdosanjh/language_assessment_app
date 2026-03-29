import os
import json
import streamlit as st
import whisper
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel

AUDIO_DIR = "assets/audio"
JSON_DIR = "exercises"

os.makedirs(JSON_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. Load Whisper model
# ---------------------------------------------------------
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

whisper_model = load_whisper()


# ---------------------------------------------------------
# 2. Transcribe audio
# ---------------------------------------------------------
def transcribe_audio(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result["text"]


# ---------------------------------------------------------
# 3. Generate 10 MCQs using Gemini (updated API)
# ---------------------------------------------------------


def generate_mcqs(transcript):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    configure(api_key=api_key)

    prompt = f"""
    You are an expert English teacher.

    Based on the following transcript, generate EXACTLY 10 multiple-choice questions.
    Each question must include:
    - "question"
    - "options" (4 options)
    - "answer" (correct option)

    Transcript:
    {transcript}

    Return ONLY valid JSON in this format:
    {{
        "questions": [
            {{
                "question": "...",
                "options": ["A", "B", "C", "D"],
                "answer": "A"
            }}
        ]
    }}
    """

    model = GenerativeModel(model_name="gemini-2.0-flash")

    response = model.generate_content(
        contents=prompt
    )

    return json.loads(response.text)["questions"]

# ---------------------------------------------------------
# 4. Build full JSON structure
# ---------------------------------------------------------
def build_json(audio_filename, transcript, mcqs):
    base = audio_filename.replace(".mp3", "")

    return {
        "listening": {
            "transcript": transcript,
            "questions": mcqs
        },
        "speaking": {
            "prompts": [
                {"task": f"Speak about the topic in '{base}' for 30 seconds."},
                {"task": "Describe one key point you remember."}
            ]
        },
        "reading": {
            "passage": f"This reading passage is linked to the audio '{base}'.",
            "questions": [
                {
                    "question": f"What is the theme of '{base}'?",
                    "options": ["Theme A", "Theme B", "Theme C", "Theme D"],
                    "answer": "Theme A"
                }
            ]
        },
        "writing": {
            "tasks": [
                {"prompt": f"Write a short summary of the audio '{base}'."},
                {"prompt": "Write your opinion about the topic."}
            ]
        }
    }


# ---------------------------------------------------------
# 5. Generate JSON for one file
# ---------------------------------------------------------
def generate_json_for_file(mp3_filename):
    audio_path = os.path.join(AUDIO_DIR, mp3_filename)

    transcript = transcribe_audio(audio_path)
    mcqs = generate_mcqs(transcript)

    json_data = build_json(mp3_filename, transcript, mcqs)

    json_filename = mp3_filename.replace(".mp3", ".json")
    json_path = os.path.join(JSON_DIR, json_filename)

    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=4)

    return json_filename, json_data


# ---------------------------------------------------------
# 6. Streamlit UI
# ---------------------------------------------------------
def json_generator_ui():
    st.header("🎧 AI‑Powered Audio → JSON Generator")

    mp3_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]

    if not mp3_files:
        st.warning("No .mp3 files found in the audio folder.")
        return

    selected = st.selectbox("Select an audio file", mp3_files)

    if st.button("Generate AI‑Powered JSON"):
        json_filename, json_data = generate_json_for_file(selected)
        st.success(f"Generated: {json_filename}")
        st.json(json_data)

        st.download_button(
            label="Download JSON",
            data=json.dumps(json_data, indent=4),
            file_name=json_filename,
            mime="application/json"
        )
