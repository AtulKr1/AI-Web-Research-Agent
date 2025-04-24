import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- CONFIGURATION ---
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]

# --- SEARCH USING SERPAPI ---
def google_search(query, num_results=5):
    search_url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        results = [result.get("link") for result in data.get("organic_results", []) if result.get("link")]
        return results
    except Exception as e:
        st.error(f"[Search Error]: {e}")
        return []

# --- SCRAPE WEB PAGE CONTENT ---
def scrape_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        texts = soup.stripped_strings
        clean_text = " ".join(texts)
        return clean_text[:4000]
    except Exception as e:
        st.error(f"[Scraping error at {url}]: {e}")
        return ""

# --- SUMMARIZE USING COHERE ---
def summarize_with_cohere(text):
    try:
        url = "https://api.cohere.ai/v1/summarize"
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "length": "medium",
            "format": "paragraph",
            "model": "command",
            "extractiveness": "auto",
            "temperature": 0.3,
            "text": text
        }
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        return result.get("summary", "[Error generating summary]")
    except Exception as e:
        st.error(f"[Summarization error]: {e}")
        return "[Error generating summary]"

# --- SYNTHESIZE MULTIPLE SUMMARIES ---
def synthesize_information(summaries):
    combined_text = "\n".join(summaries)
    return summarize_with_cohere(combined_text)

# --- STREAMLIT APP ---
def main():
    st.set_page_config(page_title="🧠 AI Web Research Agent", layout="wide")
    st.title("🧠 AI Web Research Agent")
    st.markdown("Enter a research topic below, and let AI fetch and summarize the web for you.")

    query = st.text_input("🔍 Enter your research topic:")

    if st.button("Run Research"):
        if not query:
            st.warning("Please enter a topic.")
            return

        with st.spinner("Searching and analyzing..."):
            urls = google_search(query)
            if not urls:
                st.error("No URLs found.")
                return

            summaries = []
            for i, url in enumerate(urls):
                st.markdown(f"### [{i+1}] Scraping: {url}")
                content = scrape_content(url)
                if not content:
                    continue
                summary = summarize_with_cohere(content)
                summaries.append(summary)
                time.sleep(2)

        if summaries:
            st.success("Research Completed!")

            st.subheader("Individual Source Summaries:")
            for i, summary in enumerate(summaries, 1):
                st.markdown(f"**Source {i}**: {summary}")

            st.subheader("Synthesized Report:")
            final_report = synthesize_information(summaries)
            st.write(final_report)
        else:
            st.error("No relevant summaries found.")

if __name__ == "__main__":
    main()
