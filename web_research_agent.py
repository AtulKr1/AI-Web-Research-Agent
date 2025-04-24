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

# --- STREAMLIT APP ---
def main():
    st.set_page_config(page_title="Web Research Agent", layout="wide")
    st.title("🌐 Web Research Agent")
    st.subheader("Automated research with Google Search + Summarization")

    query = st.text_input("Enter your research topic", placeholder="e.g., Social Media: Boon or Bane")

    if st.button("🔍 Run Research"):
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
                summaries.append((url, summary))
                time.sleep(2)

        st.success("✅ Research Completed!")
        for i, (url, summary) in enumerate(summaries):
            st.markdown(f"---\n### 🔹 Source {i+1}\n🔗 [{url}]({url})")
            st.markdown(summary)

if __name__ == "__main__":
    main()
