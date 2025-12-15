# AI Research Assistant (LangChain Orchestration)

This project demonstrates an **AI Research Assistant** capable of performing targeted summarization of web pages.

it includes implementation of a **LangChain Expression Language (LCEL)** pipeline that orchestrates a multi-step process:

## ✨ Core Workflow: Scrape → Prompt → Generate

1.  **Scrape:** Fetches and cleans content from a URL using `BeautifulSoup` and `requests`.
2.  **Orchestrate (LangChain):** Chains the scraped content and the user's question into a single flow.
3.  **Generate:** Uses the **Gemini 2.5 Flash API** to analyze the text and produce a specific, targeted summary.

## 🛠️ Tech Stack

* **Orchestration:** `langchain` (LCEL)
* **LLM:** `google-genai` (Gemini-2.5-Flash)
* **Frontend:** `Streamlit`
* **Data Handling:** `BeautifulSoup`, `requests`, `python-dotenv`

