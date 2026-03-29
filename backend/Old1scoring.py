import os

# Detect if running on Streamlit Cloud
RUNNING_IN_STREAMLIT_CLOUD = os.environ.get("STREAMLIT_RUNTIME", "") != ""

if RUNNING_IN_STREAMLIT_CLOUD:
    # ---------------------------------------------------------
    # SAFE FALLBACK (NO Java, NO LanguageTool)
    # ---------------------------------------------------------
    class DummyTool:
        def check(self, text):
            return []  # No grammar errors detected

    tool = DummyTool()

else:
    # ---------------------------------------------------------
    # FULL LanguageTool (LOCAL MACHINE ONLY)
    # ---------------------------------------------------------
    import language_tool_python
    tool = language_tool_python.LanguageTool('en-IN')


# ---------------------------------------------------------
# SPEAKING SCORE
# ---------------------------------------------------------
def score_speaking(transcript, keywords):
    score = 0
    for word in keywords:
        if word.lower() in transcript.lower():
            score += 1
    return score


# ---------------------------------------------------------
# WRITING SCORE
# ---------------------------------------------------------
def score_writing(text):
    matches = tool.check(text)
    penalty = len(matches)
    return max(0, 10 - penalty)
