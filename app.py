# app.py
import streamlit as st
from scrape import scrape_text_from_url
from chain import make_llm, research_summary_from_text
from utils import clean_user_input
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="AI Research Assistant", layout="centered")

st.title("AI Research Assistant — Streamlit + LangChain")
st.write("Enter a URL and a query. The app will scrape the page and summarize findings relevant to your query.")

with st.form("research_form"):
    url = st.text_input("URL to scrape", placeholder="https://example.com/article")
    query = st.text_input("Research query (e.g., 'latest trends in AI hardware')", placeholder="What do I need to know?")
    submit = st.form_submit_button("Run Research")

if submit:
    url = url.strip()
    query = clean_user_input(query)
    if not url:
        st.error("Please provide a URL to scrape.")
    elif not query:
        st.error("Please provide a question or query.")
    else:
        st.info("Scraping the page...")
        try:
            scraped = scrape_text_from_url(url)
        except Exception as e:
            st.error(f"Scraping failed: {e}")
            scraped = None

        if scraped:
            st.success("Scrape complete. Running LLM...")
            # instantiate LLM (could cache in production)
            llm = make_llm()
            try:
                result = research_summary_from_text(llm, query, scraped)
                st.markdown("### Model Output")
                st.write(result)
                with st.expander("Raw scraped text (truncated)"):
                    st.write(scraped[:2000] + ("..." if len(scraped) > 2000 else ""))
            except Exception as e:
                st.error(f"LLM call failed: {e}")
