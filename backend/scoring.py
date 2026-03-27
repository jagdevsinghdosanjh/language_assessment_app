import language_tool_python

tool = language_tool_python.LanguageTool('en-IN')

def score_speaking(transcript, keywords):
    score = 0
    for word in keywords:
        if word.lower() in transcript.lower():
            score += 1
    return score

def score_writing(text):
    matches = tool.check(text)
    penalty = len(matches)
    return max(0, 10 - penalty)
