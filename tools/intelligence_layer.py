# tools/intelligence_layer.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from typing import Dict, Any
from langchain.agents import Tool

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def scrape_recent_news(company_name: str) -> list:
    query = f"{company_name} latest news site:news.google.com"
    search_url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
    res = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('a.result__a')[:5]
    return [link.get_text(strip=True) for link in links]

def enrich_company_profile(company: Dict[str, Any]) -> Dict[str, Any]:
    name: str = company.get("name", "Unknown")
    domain: str = company.get("domain", "")
    news = scrape_recent_news(name)
    return {
        "company": name,
        "domain": domain,
        "news": news,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def _news_tool_fn(company_name: str) -> str:
    news = scrape_recent_news(company_name)
    return "\n".join(news) if news else "No recent news found."

def _intel_tool_fn(input_str: str) -> str:
    try:
        company = eval(input_str) if isinstance(input_str, str) else input_str
        profile = enrich_company_profile(company)
        return str(profile)
    except Exception as e:
        return f"Error parsing input or enriching company profile: {e}"

intelligence_tools = [
    Tool(
        name="get_recent_news",
        func=_news_tool_fn,
        description="Get 3–5 latest news headlines about a company. Input should be the company name as a string."
    ),
    Tool(
        name="enrich_company_profile",
        func=_intel_tool_fn,
        description="Get deep company profile (name, domain, recent news, timestamp). Input should be a dictionary string with 'name' and optionally 'domain'."
    )
]
