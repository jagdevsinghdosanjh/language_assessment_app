import os
import json
import subprocess
import streamlit as st
import whisper
import ollama
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()

AUDIO_DIR = "assets/audio"
JSON_DIR = "exercises"

os.makedirs(JSON_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. Load Whisper model (cached)
# ---------------------------------------------------------
@st.cache_resource
def load_whisper():
    return whisper.load_model("large-v3")

whisper_model = load_whisper()

# ---------------------------------------------------------
# 2. Preprocess audio using FFmpeg
# ---------------------------------------------------------
def preprocess_audio(input_path, output_path="temp.wav"):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path,
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path

# ---------------------------------------------------------
# 3. Transcribe audio using Whisper
# ---------------------------------------------------------
def transcribe_audio(audio_path):
    clean_audio = preprocess_audio(audio_path)
    result = whisper_model.transcribe(clean_audio)
    return result["text"]

# ---------------------------------------------------------
# 4. Generate MCQs using Ollama (llama3.1)
# ---------------------------------------------------------
def generate_mcqs(transcript):
    cleaned = transcript.replace("\n", " ").strip()

    prompt = f"""
You are an expert English comprehension teacher.

Generate EXACTLY 10 multiple-choice questions based ONLY on the transcript below.

Rules:
- Questions must be specific to the transcript.
- Avoid generic questions.
- Each question must have 4 options.
- Provide the correct answer.
- Return ONLY valid JSON.

Transcript:
{cleaned}

Return JSON in this format:
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

    response = ollama.generate(
        model="llama3.1",
        prompt=prompt
    )

    raw = response.get("response", "")

    try:
        data = json.loads(raw)
        return data.get("questions", [])
    except Exception:
        return [
            {
                "question": "Error parsing AI output.",
                "options": ["See transcript"] * 4,
                "answer": "See transcript",
            }
        ]

# ---------------------------------------------------------
# 5. Build final JSON structure
# ---------------------------------------------------------
def build_json(audio_filename, transcript, mcqs):
    base = audio_filename.replace(".mp3", "")

    return {
        "listening": {
            "transcript": transcript,
            "questions": mcqs,
        },
        "speaking": {
            "prompts": [
                {"task": f"Speak about the topic in '{base}' for 30 seconds."},
                {"task": "Describe one key point you remember."},
            ]
        },
        "reading": {
            "passage": f"This reading passage is linked to the audio '{base}'.",
            "questions": [
                {
                    "question": f"What is the theme of '{base}'?",
                    "options": ["Theme A", "Theme B", "Theme C", "Theme D"],
                    "answer": "Theme A",
                }
            ],
        },
        "writing": {
            "tasks": [
                {"prompt": f"Write a short summary of the audio '{base}'."},
                {"prompt": "Write your opinion about the topic."},
            ]
        },
    }

# ---------------------------------------------------------
# 6. Generate JSON for a single audio file
# ---------------------------------------------------------
def generate_json_for_file(mp3_filename):
    audio_path = os.path.join(AUDIO_DIR, mp3_filename)

    transcript = transcribe_audio(audio_path)
    mcqs = generate_mcqs(transcript)

    json_data = build_json(mp3_filename, transcript, mcqs)

    json_filename = mp3_filename.replace(".mp3", ".json")
    json_path = os.path.join(JSON_DIR, json_filename)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return json_filename, json_data

# ---------------------------------------------------------
# 7. Streamlit UI
# ---------------------------------------------------------
def json_generator_ui():
    st.header("🎧 AI‑Powered Audio → JSON Generator (Ollama Offline)")

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
            data=json.dumps(json_data, indent=4, ensure_ascii=False),
            file_name=json_filename,
            mime="application/json",
        )
