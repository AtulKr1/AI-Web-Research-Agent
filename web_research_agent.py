import requests
from bs4 import BeautifulSoup
import time

# --- CONFIGURATION ---
SERPAPI_KEY = "3ca3beb27a7c2f9d75e4ba73f4afabecbbb8fcd200f7938496b419a14d7e181e"  # Replace with your SerpAPI key
COHERE_API_KEY = "3LHrrGJ5XyITCibcsqdRz23T05fAKlRmYpnrITx5"  # Replace with your Cohere API key

# --- SEARCH USING SERPAPI ---
def google_search(query, num_results=5):
    print("🔍 Searching the web...\n")
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
        print("Found URLs:", results)
        return results
    except Exception as e:
        print(f"[Search Error]: {e}")
        return []

# --- SCRAPE WEB PAGE CONTENT ---
def scrape_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()  # Check if request was successful
        soup = BeautifulSoup(page.content, "html.parser")

        # Get only visible text (basic strategy)
        texts = soup.stripped_strings
        clean_text = " ".join(texts)
        return clean_text[:4000]  # Keep length within Cohere limits
    except requests.exceptions.RequestException as e:
        print(f"[Scraping error at {url}]: {e}")
        return ""
    except Exception as e:
        print(f"[General error at {url}]: {e}")
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
        response.raise_for_status()  # Ensure successful response
        result = response.json()
        return result.get("summary", "[Error generating summary]")
    except requests.exceptions.RequestException as e:
        print(f"[Summarization error]: {e}")
        return "[Error generating summary]"
    except Exception as e:
        print(f"[General error in summarization]: {e}")
        return "[Error generating summary]"

# --- MAIN RESEARCH FUNCTION ---
def run_research_agent():
    query = input("Enter your research topic: ").strip()
    urls = google_search(query)

    if not urls:
        print("[No URLs found. Exiting.]\n")
        return

    summaries = []
    for i, url in enumerate(urls):
        print(f"\n[{i+1}] Scraping: {url}")
        content = scrape_content(url)
        if not content:
            print(f"   ➤ No content scraped from {url}. Skipping.\n")
            continue
        print(f"   ➤ Scraped {len(content)} characters")

        summary = summarize_with_cohere(content)
        summaries.append(f"🔹 Source {i+1} Summary:\n{summary}\n")

        time.sleep(2)  # Be polite with rate limiting

    print("\n📘 Consolidated Research Report:\n")
    if summaries:
        for s in summaries:
            print(s)
    else:
        print("[No relevant summaries found.]")

# --- RUN SCRIPT ---
if __name__ == "__main__":
    run_research_agent()
