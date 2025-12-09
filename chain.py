# chain.py
import os
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from utils import safe_truncate

load_dotenv()  # loads GOOGLE_API_KEY from .env

def make_llm(model_name="gemini-2.0-flash", temperature=0.0):
    """
    Returns a LangChain LLM wrapper for Google generative model.
    The google-genai SDK expects GOOGLE_API_KEY env var.
    """
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
    return llm

def research_summary_from_text(llm, query, scraped_text):
    """
    Given an LLM instance, a user query, and scraped text,
    return a short structured research output.
    """
    # Truncate text to a safe size (so prompt fits tokens)
    content = safe_truncate(scraped_text, max_chars=3000)

    prompt = f"""
You are an AI research assistant.

User query:
{query}

Context (extracted from a webpage):
{content}

Please:
1) Provide a brief (3-6 sentence) summary focused on the query.
2) List 3 key points/facts relevant to the query (bullet points).
3) Provide 2 suggested follow-up queries or next steps.

Return output in clear sections labeled SUMMARY, KEY_POINTS, NEXT_STEPS.
"""

    # LangChain expects messages
    human_msg = HumanMessage(content=prompt)
    resp = llm.predict_messages([human_msg])  # returns a ChatMessage
    return resp.content
