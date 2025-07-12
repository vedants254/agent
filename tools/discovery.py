import os
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from langchain.tools.base import BaseTool

@dataclass
class Company:
    name: str
    domain: str = ""
    industry: str = ""
    location: str = ""
    phone: str = ""
    rating: float = 0.0

class GooglePlacesTool(BaseTool):
    name: str = "google_places_discovery"
    description: str = "Use this to search businesses using Google Places API. Input is a query like 'textile importers in Dubai'. Returns name, website, industry, location."

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key or os.getenv("GOOGLE_PLACES_API_KEY")
        if not self.api_key:
            raise ValueError("Google Places API key not found. Set GOOGLE_PLACES_API_KEY environment variable.")
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.session = requests.Session()

    def _run(self, query: str) -> str:
        companies = self._search_companies(query)
        results = []
        for c in companies:
            result_str = f"""
            Company: {c.name}
            Website: {c.domain or 'N/A'}
            Industry: {c.industry or 'N/A'}
            Location: {c.location or 'N/A'}
            """
            results.append(result_str.strip())
        return "\n---\n".join(results) or "No matching companies found."

    def _search_companies(self, query: str, max_results: int = 5) -> List[Company]:
        places = self._text_search(query, max_results)
        companies = []
        for place in places:
            place_id = place.get("place_id")
            details = self._get_place_details(place_id) if place_id else {}
            company = self._make_company(place, details)
            if company:
                companies.append(company)
        return companies

    def _text_search(self, query: str, max_results: int) -> List[Dict]:
        url = f"{self.base_url}/textsearch/json"
        params = {
            "query": query,
            "key": self.api_key,
            "type": "establishment",
            "language": "en"
        }

        all_places = []
        next_page_token = None

        while len(all_places) < max_results:
            if next_page_token:
                params["pagetoken"] = next_page_token
            res = self.session.get(url, params=params, timeout=10).json()
            if res.get("status") != "OK":
                break
            all_places.extend(res.get("results", []))
            next_page_token = res.get("next_page_token")
            if not next_page_token:
                break

        return all_places[:max_results]

    def _get_place_details(self, place_id: str) -> Dict:
        url = f"{self.base_url}/details/json"
        params = {
            "place_id": place_id,
            "key": self.api_key,
            "fields": "name,website,formatted_phone_number,formatted_address,types,rating",
            "language": "en"
        }
        return self.session.get(url, params=params, timeout=10).json().get("result", {})

    def _make_company(self, place: Dict, details: Dict) -> Optional[Company]:
        name = place.get("name")
        if not name:
            return None

        location = place.get("formatted_address") or details.get("formatted_address", "")
        types = place.get("types") or details.get("types", [])
        industry = self._format_types(types)
        rating = place.get("rating") or details.get("rating", 0.0)
        website = details.get("website", "")
        domain = self._extract_domain(website) if website else ""
        phone = details.get("formatted_phone_number", "")

        return Company(name=name, domain=domain, industry=industry, location=location, phone=phone, rating=rating)

    def _format_types(self, types: List[str]) -> str:
        skip = {"point_of_interest", "establishment", "premise", "subpremise", "route", "political", "locality", "country"}
        return ", ".join([t.replace("_", " ").title() for t in types if t not in skip][:3])

    def _extract_domain(self, url: str) -> str:
        url = url.replace("https://", "").replace("http://", "").replace("www.", "")
        return url.split("/")[0].split("?")[0]
    



disccovery_tools = [GooglePlacesTool()]
