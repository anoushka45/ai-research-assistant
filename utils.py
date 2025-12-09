# utils.py
import re

def safe_truncate(text, max_chars=3000):
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    # try to cut at sentence boundary
    snippet = text[:max_chars]
    # find last period to try keep full sentence
    last_dot = snippet.rfind(".")
    if last_dot != -1 and last_dot > max_chars*0.6:
        return snippet[:last_dot+1]
    return snippet

def clean_user_input(s):
    # basic cleaning for query
    if not s:
        return ""
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s
