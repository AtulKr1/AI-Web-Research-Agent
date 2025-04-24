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

# Documentation

## Overview

This project is an **AI-powered web research agent** built using Python, Streamlit, and external APIs. The agent automates the process of searching the web, scraping web page content, and summarizing the information using the **Cohere API**.

The app uses **SerpAPI** to perform Google search and fetch a list of relevant URLs. The content from these URLs is then scraped using **BeautifulSoup** and summarized using **Cohere AI**.

## How It Works

### Google Search:

- The app starts by accepting a research topic input from the user.
- The input is used to query **SerpAPI** for a list of relevant URLs.

### Web Scraping:

- The app fetches the content of the URLs using **requests** and parses them using **BeautifulSoup** to cleanly extract text from the web page.

### Summarization:

- The content scraped from each page is sent to **Cohere's API** for summarization.
- The summarization is then displayed to the user.

### Synthesis:

- All individual summaries are combined into one text block.
- This block is sent to **Cohere's API** for a final synthesized report.

### Streamlit Interface:

- The user interacts with the system through a **Streamlit** interface where they can input research topics and view the results.

## File Structure

- `web_research_agent.py`: The main Streamlit app that handles user interaction, API requests, and result display.
- `requirements.txt`: Contains all the Python dependencies needed for the app.
- `README.md`: This documentation file.
- `.streamlit/secrets.toml`: A secure file to store your **SerpAPI** and **Cohere API** keys.

## Libraries Used

- **Streamlit**: For creating the user interface.
- **Requests**: For making HTTP requests to APIs and web pages.
- **BeautifulSoup**: For parsing and scraping content from web pages.
- **Cohere API**: For summarizing the web content.

