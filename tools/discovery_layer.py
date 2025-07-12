import os
import requests
import spacy
from langchain.tools.base import BaseTool
from langchain.tools.ddg_search.tool import DuckDuckGoSearchRun

APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
nlp = spacy.load("en_core_web_sm")

class ApolloCompanySearchTool(BaseTool):
    name: str = "apollo_company_search"
    description: str = "Search companies using Apollo API with keyword and location filters."

    def _extract_keyword_and_location(self, text):
        doc = nlp(text)
        location = None
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                location = ent.text
                break
        keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.text != location]
        return " ".join(keywords).strip(), location

    def _run(self, query: str) -> str:
        keyword, location = self._extract_keyword_and_location(query)
        payload = {
            "api_key": APOLLO_API_KEY,
            "q_organization_keywords": keyword,
            "organization_num_employees_ranges": ["11-50", "51-200"],
            "page": 1
        }
        if location:
            payload["q_organization_locations"] = [location]
        res = requests.post("https://api.apollo.io/v1/accounts/search", json=payload, timeout=10)
        companies = res.json().get("accounts", [])[:5]
        results = []
        for c in companies:
            name = c.get("name")
            domain = c.get("website_url")
            industry = c.get("industry", "")
            loc = c.get("location", "")
            if domain:
                enrich = requests.post(
                    "https://api.apollo.io/v1/organizations/enrich",
                    json={"api_key": APOLLO_API_KEY, "domain": domain},
                    timeout=10
                ).json().get("organization", {})
                industry = enrich.get("industry") or industry
                loc = enrich.get("location_name") or loc
            result = f"""
            Company: {name}
            Website: {domain}
            Industry: {industry or 'N/A'}
            Location: {loc or 'N/A'}
            """
            results.append(result.strip())
        return "\n---\n".join(results) or "No matching companies found."

class DuckDuckGoCompanySearchTool(BaseTool):
    name: str = "duckduckgo_company_search"
    description: str = "Fallback search for companies using DuckDuckGo."

    def _run(self, query: str) -> str:
        ddg = DuckDuckGoSearchRun()
        return f"DuckDuckGo search results for '{query}':\n" + ddg.run(query)

discovery_tools = [ApolloCompanySearchTool(), DuckDuckGoCompanySearchTool()]
