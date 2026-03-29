import streamlit as st
from streamlit.components.v1 import html  # noqa
from backend.scoring import score_speaking, score_writing  # noqa
import json
import os

# Correct import for JSON generator
from modules.json_generator import json_generator_ui


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Language Skills Assessment", layout="wide")

st.title("Language Skills Assessment System")
st.write("Listening • Speaking • Reading • Writing")


# ---------------------------------------------------------
# SIDEBAR MENU
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "Select Test",
    ["Listening", "Speaking", "Reading", "Writing", "JSON Generator"]
)


# ---------------------------------------------------------
# LISTENING MODULE
# ---------------------------------------------------------
if menu == "Listening":
    st.header("Listening Test")

    audio_dir = "assets/audio"
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]

    if not audio_files:
        st.error("No audio files found in assets/audio/")
        st.stop()

    selected_audio = st.selectbox("Choose a Listening Test", audio_files)

    json_name = selected_audio.replace(".mp3", ".json")
    json_path = os.path.join("exercises", json_name)

    if not os.path.exists(json_path):
        st.warning(f"No JSON found for {selected_audio}. Please generate it using JSON Generator.")
        st.stop()

    # Load JSON safely
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            listening_data = json.load(f)
    except Exception:
        st.error("Error reading JSON file. Please regenerate it.")
        st.stop()

    exercise = listening_data.get("listening", {})

    if "questions" not in exercise or not exercise["questions"]:
        st.error("No questions found in JSON. Please regenerate using JSON Generator.")
        st.stop()

    # Play audio
    st.audio(os.path.join(audio_dir, selected_audio))

    st.subheader("Answer the following questions:")

    user_answers = []
    correct_answers = []

    for idx, q in enumerate(exercise["questions"]):
        st.write(f"**Q{idx+1}. {q['question']}**")
        answer = st.radio(
            f"Select your answer for Q{idx+1}",
            q["options"],
            key=f"q{idx}"
        )
        user_answers.append(answer)
        correct_answers.append(q["answer"])

    if st.button("Submit"):
        score = sum([1 for u, c in zip(user_answers, correct_answers) if u == c])
        st.success(f"Your Listening Score: {score} / {len(correct_answers)}")


# ---------------------------------------------------------
# SPEAKING MODULE
# ---------------------------------------------------------
elif menu == "Speaking":
    st.header("Speaking Test")
    st.info("Speaking test module will be integrated here.")


# ---------------------------------------------------------
# READING MODULE
# ---------------------------------------------------------
elif menu == "Reading":
    st.header("Reading Test")
    st.info("Reading test module will be integrated here.")


# ---------------------------------------------------------
# WRITING MODULE
# ---------------------------------------------------------
elif menu == "Writing":
    st.header("Writing Test")
    st.info("Writing test module will be integrated here.")


# ---------------------------------------------------------
# JSON GENERATOR MODULE
# ---------------------------------------------------------
elif menu == "JSON Generator":
    json_generator_ui()
