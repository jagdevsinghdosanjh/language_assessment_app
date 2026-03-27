# 🎧📖 Language Skills Assessment System (LSRW)
A Streamlit‑based interactive web application designed to assess **Listening, Speaking, Reading, and Writing** skills using syllabus‑aligned exercises.  
Built with **Python, Streamlit, HTML, CSS, and JavaScript**, this app supports webcam/microphone input, JSON‑based question banks, and modular expansion for multiple languages.

---

## 🚀 Features

### ✅ Listening Module
- Plays MP3 audio files
- Loads MCQ questions from JSON
- Auto‑scores student responses
- Clean UI for exam‑style assessment

### 🎤 Speaking Module
- Uses browser microphone
- Speech‑to‑text via Web Speech API (JavaScript)
- Streamlit custom component integration
- Can be extended for pronunciation scoring

### 📖 Reading Module
- Displays passages from JSON
- MCQs or short‑answer questions
- Auto‑scoring logic

### ✍️ Writing Module
- Text‑area input for paragraph/letter writing
- Grammar scoring (custom or library‑based)
- Extendable rubric system

### 🗂 Modular Architecture
- Exercises stored in `/exercises/*.json`
- Audio stored in `/assets/audio/`
- Custom JS components in `/components/`
- Backend scoring logic in `/backend/`

---

## 📁 Project Structure
language_assessment_app/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── backend/
│   ├── scoring.py
│   ├── storage.py
│
├── components/
│   ├── webcam_component.html
│   ├── speech_to_text_component.html
│
├── exercises/
│   ├── listening.json
│   ├── reading.json
│
├── assets/
│   ├── styles.css
│   ├── audio/
│       ├── listening1.mp3

Code

---

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/jagdevsinghdosanjh/language_assessment_app
cd language_assessment_app
2️⃣ Create Virtual Environment (Python 3.10 Recommended)
bash
python -m venv venv
Activate it:

Windows

bash
.\venv\Scripts\activate
3️⃣ Install Dependencies
bash
pip install -r requirements.txt
4️⃣ Run the App
bash
streamlit run app.py
🧩 JSON‑Based Exercises
Listening JSON Example
json
{
  "listening": {
    "questions": [
      {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Rome"],
        "answer": "Paris"
      }
    ]
  }
}
You can add unlimited listening sets by extending the JSON.

🎨 Custom Styling
All UI styling is handled in:

Code
assets/styles.css
You can modify colors, fonts, and layout to match your school or brand.

🧪 Technologies Used
Python 3.10+

Streamlit

JavaScript (WebRTC, Web Speech API)

HTML/CSS

SQLite (optional for storage)

pydub / numpy / opencv (optional extensions)

📌 Roadmap (Upcoming Features)
Teacher dashboard for viewing scores

Student login system

Webcam video recording

AI‑based speaking evaluation

Multi‑language support (Punjabi/Hindi/English)

PDF report generation

🤝 Contributing
Pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

📄 License
This project is open‑source under the MIT License.

👨‍💻 Author
Jagdev Singh Dosanjh  
Visionary educator, developer, and architect of modular learning systems.

