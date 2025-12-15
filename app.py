import streamlit as st
import os
from research_assistant import scrape_text, research_chain

# --- STREAMLIT APP ---
def main():
    st.set_page_config(page_title="AI Research Assistant", layout="wide")
    st.title("💡AI Research Assistant")
    st.markdown("---")

    # Sidebar for API Key Management
    with st.sidebar:
        st.header("Configuration")
        
        # Get the API Key
        gemini_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            value=os.environ.get("GEMINI_API_KEY", "") # Pre-fill if already in env
        )
        
        if gemini_key:
            os.environ["GEMINI_API_KEY"] = gemini_key
            st.success("API Key loaded.")
        else:
            st.warning("Please enter your Gemini API Key.")

    # Main App Interface
    url = st.text_input(
        "🔗 Enter a URL to Research:", 
        value="https://en.wikipedia.org/wiki/Artificial_intelligence"
    )
    user_query = st.text_area(
        "❓ What specific question do you have about this page?", 
        value="Summarize the history and ethical concerns of AI."
    )

    if st.button("Start Research") and url and user_query:
        if "GEMINI_API_KEY" not in os.environ or not os.environ["GEMINI_API_KEY"]:
            st.error("Cannot start. Please provide your Gemini API Key in the sidebar.")
            return

        with st.spinner("Step 1: Scraping content..."):
            
            # --- SCRAPE STEP (research_assistant.py) ---
            raw_content = scrape_text(url)
            
            if "Error during scraping" in raw_content:
                st.error(raw_content)
                return

            st.success(f"✅ Scraped content successfully! (Length: {len(raw_content)} characters)")
            
        with st.spinner("Step 2 & 3: AI Analysis via LangChain..."):
            
            # --- PROMPT & GENERATE STEP (LangChain Chain) ---
            try:
                # Invoke the LangChain pipeline with the input dictionary
                result = research_chain.invoke({
                    "scraped_content": raw_content, 
                    "user_question": user_query
                })
                
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown("## 🔍 Research Report")
                st.write(result)
                
            except Exception as e:
                st.error(f"An error occurred during AI analysis: {e}")
                
if __name__ == "__main__":
    main()