import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate  # <--- FIX IS HERE
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
import os


from dotenv import load_dotenv
load_dotenv()

# --- 1. WEB SCRAPING FUNCTION ---
def scrape_text(url: str) -> str:
    """Fetches text content from a given URL using BeautifulSoup."""
    try:
        # Set a user-agent to mimic a real browser (optional, but can prevent some blocks)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav']):
            script_or_style.decompose()

        # Get text, strip whitespace, and join lines with a space
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Limit the size of the text passed to the LLM to avoid context window overflow
        return text_content[:10000]
        
    except requests.exceptions.Timeout:
        return "Error during scraping: The request timed out."
    except requests.exceptions.HTTPError as e:
        return f"Error during scraping: HTTP Error - {e}"
    except Exception as e:
        return f"Error during scraping: An unexpected error occurred - {e}"

# --- 2. LANGCHAIN SIMPLE CHAIN ---

# Initialize the Gemini model (it automatically uses the GEMINI_API_KEY environment variable)
# Set a low temperature for factual summary tasks
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# Define the Prompt Template
template = """
You are an expert research assistant. Your goal is to analyze the provided web page content and produce a concise, insightful summary focused on answering the user's specific question.
Cite relevant sections if possible.

WEB PAGE CONTENT:
---
{scraped_content}
---

USER QUESTION: "{user_question}"

Based ONLY on the content above, provide a comprehensive, detailed answer and a 3-point summary in markdown format.
"""

research_prompt = PromptTemplate.from_template(template)

# Build the simple chain using LCEL (LangChain Expression Language)
# This orchestrates the steps: (Input) -> Prompt -> LLM -> (Output)
research_chain = (
    # RunnablePassthrough ensures the input dictionary (with scraped_content and user_question) 
    # is passed through to the next step.
    RunnablePassthrough() 
    | research_prompt 
    | llm           
    | StrOutputParser()
)