import os
import yaml
import httpx
from typing import List, Dict

def load_searxng_url():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
    config_path = os.path.join(root_dir, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config["searxng"].get("url", "http://localhost:8080")

async def fetch_real_links(query: str, engines: str = "youtube,duckduckgo") -> List[Dict]:
    base_url = load_searxng_url()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/search",
                params={"q": query, "format": "json", "engines": engines},
                timeout=10.0
            )
            response.raise_for_status()
            results = response.json().get("results", [])
            
            # return top 3 real verified links
            verified_links = []
            for r in results[:3]:
                verified_links.append({
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "engine": r.get("engine")
                })
            return verified_links
    except Exception as e:
        print(f"SearXNG fetch failed for query '{query}': {str(e)}")
        return []
