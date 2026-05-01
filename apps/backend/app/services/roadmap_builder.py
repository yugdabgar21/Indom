from app.models.schemas import Roadmap
from app.services.searxng_search import fetch_real_links
from typing import Dict, Any

async def build_enriched_roadmap(roadmap: Roadmap) -> Dict[str, Any]:
    enriched_days = []
    for day in roadmap.days:
        links = await fetch_real_links(day.search_query)
        enriched_days.append({
            "day": day.day,
            "topic": day.topic,
            "description": day.description,
            "search_query": day.search_query,
            "resources": links
        })
    return {"days": enriched_days}
