import os
import json
import streamlit as st

AUDIO_DIR = "assets/audio"
JSON_DIR = "exercises"

os.makedirs(JSON_DIR, exist_ok=True)


# ---------------------------------------------------------
# DYNAMIC TEMPLATE — NOW GENERATES 10 QUESTIONS
# ---------------------------------------------------------
def default_template(audio_filename):
    base = audio_filename.replace(".mp3", "")

    # Generate 10 listening questions dynamically
    listening_questions = []
    for i in range(1, 10 + 1):
        listening_questions.append({
            "question": f"Q{i}. What is one key idea mentioned in the audio '{base}'?",
            "options": [
                f"Option A{i}",
                f"Option B{i}",
                f"Option C{i}",
                f"Option D{i}"
            ],
            "answer": f"Option A{i}"
        })

    return {
        "listening": {
            "questions": listening_questions
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
# GENERATE JSON FOR ONE FILE
# ---------------------------------------------------------
def generate_json_for_file(mp3_filename):
    json_data = default_template(mp3_filename)
    json_filename = mp3_filename.replace(".mp3", ".json")
    json_path = os.path.join(JSON_DIR, json_filename)

    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=4)

    return json_filename, json_data


# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
def questions_generator_ui():
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

# import os
# import json
# import streamlit as st

# AUDIO_DIR = "assets/audio"
# JSON_DIR = "exercises"

# os.makedirs(JSON_DIR, exist_ok=True)


# # ---------------------------------------------------------
# # DYNAMIC TEMPLATE — NOW GENERATES 10 QUESTIONS
# # ---------------------------------------------------------
# def default_template(audio_filename):
#     base = audio_filename.replace(".mp3", "")

#     # Generate 10 listening questions dynamically
#     listening_questions = []
#     for i in range(1, 10 + 1):
#         listening_questions.append({
#             "question": f"Q{i}. What is one key idea mentioned in the audio '{base}'?",
#             "options": [
#                 f"Option A{i}",
#                 f"Option B{i}",
#                 f"Option C{i}",
#                 f"Option D{i}"
#             ],
#             "answer": f"Option A{i}"
#         })

#     return {
#         "listening": {
#             "questions": listening_questions
#         },

#         "speaking": {
#             "prompts": [
#                 {"task": f"Speak about the topic in '{base}' for 30 seconds."},
#                 {"task": "Describe one key point you remember."}
#             ]
#         },

#         "reading": {
#             "passage": f"This reading passage is linked to the audio '{base}'.",
#             "questions": [
#                 {
#                     "question": f"What is the theme of '{base}'?",
#                     "options": ["Theme A", "Theme B", "Theme C", "Theme D"],
#                     "answer": "Theme A"
#                 }
#             ]
#         },

#         "writing": {
#             "tasks": [
#                 {"prompt": f"Write a short summary of the audio '{base}'."},
#                 {"prompt": "Write your opinion about the topic."}
#             ]
#         }
#     }


# # ---------------------------------------------------------
# # GENERATE JSON FOR ONE FILE
# # ---------------------------------------------------------
# def generate_json_for_file(mp3_filename):
#     json_data = default_template(mp3_filename)
#     json_filename = mp3_filename.replace(".mp3", ".json")
#     json_path = os.path.join(JSON_DIR, json_filename)

#     with open(json_path, "w") as f:
#         json.dump(json_data, f, indent=4)

#     return json_filename, json_data


# # ---------------------------------------------------------
# # STREAMLIT UI
# # ---------------------------------------------------------
# def json_generator_ui():
#     st.header("🎧 Audio → JSON Generator")

#     mp3_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]

#     if not mp3_files:
#         st.warning("No .mp3 files found in the audio folder.")
#         return

#     # Single file mode
#     st.subheader("Generate JSON for a single audio file")
#     selected = st.selectbox("Select an audio file", mp3_files)

#     if st.button("Generate JSON for selected file"):
#         json_filename, json_data = generate_json_for_file(selected)
#         st.success(f"Generated: {json_filename}")
#         st.json(json_data)

#         st.download_button(
#             label="Download JSON",
#             data=json.dumps(json_data, indent=4),
#             file_name=json_filename,
#             mime="application/json"
#         )

#     st.divider()

#     # Batch mode
#     st.subheader("Batch generate JSON for all audio files")

#     if st.button("Generate JSON for all .mp3 files"):
#         results = []
#         for mp3 in mp3_files:
#             json_filename, _ = generate_json_for_file(mp3)
#             results.append(json_filename)

#         st.success("Generated JSON files:")
#         st.write(results)

# # import os
# # import json
# # import streamlit as st

# # AUDIO_DIR = "assets/audio"
# # JSON_DIR = "exercises"

# # os.makedirs(JSON_DIR, exist_ok=True)


# # # ---------------------------------------------------------
# # # DYNAMIC TEMPLATE (changes per audio file)
# # # ---------------------------------------------------------
# # def default_template(audio_filename):
# #     base = audio_filename.replace(".mp3", "")

# #     return {
# #         "listening": {
# #             "questions": [
# #                 {
# #                     "question": f"What is the main idea of the audio '{base}'?",
# #                     "options": [
# #                         "Idea A",
# #                         "Idea B",
# #                         "Idea C",
# #                         "Idea D"
# #                     ],
# #                     "answer": "Idea A"
# #                 },
# #                 {
# #                     "question": f"Which detail is mentioned in '{base}'?",
# #                     "options": [
# #                         "Detail A",
# #                         "Detail B",
# #                         "Detail C",
# #                         "Detail D"
# #                     ],
# #                     "answer": "Detail A"
# #                 }
# #             ]
# #         },

# #         "speaking": {
# #             "prompts": [
# #                 {"task": f"Speak about the topic in '{base}' for 30 seconds."},
# #                 {"task": "Describe one key point you remember."}
# #             ]
# #         },

# #         "reading": {
# #             "passage": f"This reading passage is linked to the audio '{base}'.",
# #             "questions": [
# #                 {
# #                     "question": f"What is the theme of '{base}'?",
# #                     "options": ["Theme A", "Theme B", "Theme C", "Theme D"],
# #                     "answer": "Theme A"
# #                 }
# #             ]
# #         },

# #         "writing": {
# #             "tasks": [
# #                 {"prompt": f"Write a short summary of the audio '{base}'."},
# #                 {"prompt": "Write your opinion about the topic."}
# #             ]
# #         }
# #     }


# # # ---------------------------------------------------------
# # # GENERATE JSON FOR ONE FILE
# # # ---------------------------------------------------------
# # def generate_json_for_file(mp3_filename):
# #     json_data = default_template(mp3_filename)
# #     json_filename = mp3_filename.replace(".mp3", ".json")
# #     json_path = os.path.join(JSON_DIR, json_filename)

# #     with open(json_path, "w") as f:
# #         json.dump(json_data, f, indent=4)

# #     return json_filename, json_data


# # # ---------------------------------------------------------
# # # STREAMLIT UI
# # # ---------------------------------------------------------
# # def questions_generator_ui():
# #     st.header("🎧 Audio → JSON Generator")

# #     mp3_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]

# #     if not mp3_files:
# #         st.warning("No .mp3 files found in the audio folder.")
# #         return

# #     # Single file mode
# #     st.subheader("Generate JSON for a single audio file")
# #     selected = st.selectbox("Select an audio file", mp3_files)

# #     if st.button("Generate JSON for selected file"):
# #         json_filename, json_data = generate_json_for_file(selected)
# #         st.success(f"Generated: {json_filename}")
# #         st.json(json_data)

# #         st.download_button(
# #             label="Download JSON",
# #             data=json.dumps(json_data, indent=4),
# #             file_name=json_filename,
# #             mime="application/json"
# #         )

# #     st.divider()

# #     # Batch mode
# #     st.subheader("Batch generate JSON for all audio files")

# #     if st.button("Generate JSON for all .mp3 files"):
# #         results = []
# #         for mp3 in mp3_files:
# #             json_filename, _ = generate_json_for_file(mp3)
# #             results.append(json_filename)

# #         st.success("Generated JSON files:")
# #         st.write(results)
