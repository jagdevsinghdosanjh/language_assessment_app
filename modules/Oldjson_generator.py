import os
import json
import streamlit as st

AUDIO_DIR = "assets/audio"
JSON_DIR = "exercises"

os.makedirs(JSON_DIR, exist_ok=True)

def default_template():
    return {
        "listening": {
            "questions": [
                {
                    "question": "What is the capital of France?",
                    "options": ["Paris", "London", "Berlin", "Rome"],
                    "answer": "Paris"
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Earth", "Mars", "Jupiter", "Venus"],
                    "answer": "Mars"
                }
            ]
        },
        "speaking": {
            "prompts": [
                {"task": "Introduce yourself in 2–3 sentences."},
                {"task": "Describe your favorite hobby and why you enjoy it."}
            ]
        },
        "reading": {
            "passage": "Once upon a time, a prince lived in a grand palace. He was admired by all, but he longed to see the world beyond his walls.",
            "questions": [
                {
                    "question": "Where did the prince live?",
                    "options": ["In a cottage", "In a palace", "In a forest", "In a village"],
                    "answer": "In a palace"
                },
                {
                    "question": "What did the prince long to do?",
                    "options": ["See the world", "Build a palace", "Meet his people", "Travel to the forest"],
                    "answer": "See the world"
                }
            ]
        },
        "writing": {
            "tasks": [
                {"prompt": "Write a short paragraph about your favorite season."},
                {"prompt": "Compose a letter to your friend describing a recent trip."}
            ]
        }
    }


def generate_json_for_file(mp3_filename):
    json_data = default_template()
    json_filename = mp3_filename.replace(".mp3", ".json")
    json_path = os.path.join(JSON_DIR, json_filename)

    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=4)

    return json_filename, json_data


def json_generator_ui():
    st.header("🎧 Audio → JSON Generator")

    mp3_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]

    if not mp3_files:
        st.warning("No .mp3 files found in the audio folder.")
        return

    # Single file mode
    st.subheader("Generate JSON for a single audio file")
    selected = st.selectbox("Select an audio file", mp3_files)

    if st.button("Generate JSON for selected file"):
        json_filename, json_data = generate_json_for_file(selected)
        st.success(f"Generated: {json_filename}")
        st.json(json_data)

        st.download_button(
            label="Download JSON",
            data=json.dumps(json_data, indent=4),
            file_name=json_filename,
            mime="application/json"
        )

    st.divider()

    # Batch mode
    st.subheader("Batch generate JSON for all audio files")

    if st.button("Generate JSON for all .mp3 files"):
        results = []
        for mp3 in mp3_files:
            json_filename, _ = generate_json_for_file(mp3)
            results.append(json_filename)

        st.success("Generated JSON files:")
        st.write(results)
