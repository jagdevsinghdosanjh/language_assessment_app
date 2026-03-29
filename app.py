import streamlit as st
from streamlit.components.v1 import html #noqa
from backend.scoring import score_speaking, score_writing #noqa
import json
import os


st.set_page_config(page_title="Language Skills Assessment", layout="wide")

st.title("Language Skills Assessment System")
st.write("Listening • Speaking • Reading • Writing")
with open("exercises/listening.json", "r", encoding="utf-8") as f:
    listening_data = json.load(f)


menu = st.sidebar.radio("Select Test", ["Listening", "Speaking", "Reading", "Writing"])

if menu == "Listening":
    st.header("Listening Test")

    # Load exercise
    exercise = listening_data["listening"]

    # Play audio
    audio_path = os.path.join("assets", "audio", "listening1.mp3")
    st.audio(audio_path)

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



# if menu == "Listening":
#     st.header("Listening Test")
#     st.audio("assets/audio/listening1.mp3")
#     answer = st.text_input("Write your answer")
#     if st.button("Submit"):
#         st.success("Response saved!")

# elif menu == "Speaking":
#     st.header("Speaking Test")
#     st.write("Click Start to begin recording")

#     with open("components/speech_to_text_component.html") as f:
#         html(f.read(), height=300)

# elif menu == "Reading":
#     st.header("Reading Test")
#     st.write("Read the passage and answer questions")

# elif menu == "Writing":
#     st.header("Writing Test")
#     text = st.text_area("Write your paragraph here")
#     if st.button("Evaluate"):
#         score = score_writing(text)
#         st.success(f"Writing Score: {score}/10")
