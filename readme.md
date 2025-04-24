# AI Web Research Agent

A Streamlit-powered app that performs automatic web research using Google search (via SerpAPI), content scraping (via BeautifulSoup), and summarization (via Cohere AI).

## Features

- Google Search integration via SerpAPI
- Web scraping using BeautifulSoup
- Text summarization using Cohere's AI
- Clean Streamlit UI

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- Requests
- BeautifulSoup4
- SerpAPI key
- Cohere API key

### Installation

```bash
git clone https://github.com/your-username/ai-web-research-agent.git
cd ai-web-research-agent
pip install -r requirements.txt
```
## Running the App

```bash
streamlit run web_research_agent.py
```

## Setting up Secrets

```bash
SERPAPI_KEY = "your-serpapi-key"
COHERE_API_KEY = "your-cohere-api-key"
```
