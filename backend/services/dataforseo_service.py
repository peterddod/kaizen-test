import httpx
import base64
from typing import List, Dict
from config import settings
import logging

logger = logging.getLogger(__name__)

class DataForSEOService:
    def __init__(self):
        self.base_url = "https://api.dataforseo.com/v3"
        credentials = f"{settings.DATAFORSEO_LOGIN}:{settings.DATAFORSEO_PASSWORD}"
        self.auth_header = base64.b64encode(credentials.encode()).decode()
    
    async def get_serp_results(self, keyword: str, location: str = "Ireland") -> List[Dict]:
        try:
            logger.info(f"Fetching SERP results for keyword: {keyword}")
            
            endpoint = f"{self.base_url}/serp/google/organic/live/regular"
            
            headers = {
                "Authorization": f"Basic {self.auth_header}",
                "Content-Type": "application/json"
            }
            
            payload = [{
                "keyword": keyword,
                "location_name": location,
                "language_name": "English",
                "device": "desktop",
                "os": "windows",
                "depth": 10
            }]
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(endpoint, json=payload, headers=headers)
            
            logger.info(f"DataForSEO response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if data.get("tasks") and len(data["tasks"]) > 0:
                    task = data["tasks"][0]
                    if task.get("result") and len(task["result"]) > 0:
                        items = task["result"][0].get("items", [])
                        
                        for idx, item in enumerate(items[:10]):
                            if item.get("type") == "organic":
                                results.append({
                                    "position": idx + 1,
                                    "url": item.get("url", ""),
                                    "title": item.get("title", ""),
                                    "description": item.get("description", "")
                                })
                
                logger.info(f"Found {len(results)} organic results")
                return results
            else:
                error_msg = f"DataForSEO API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                # Return empty results instead of failing
                return []
                
        except Exception as e:
            logger.error(f"Error fetching SERP results: {str(e)}")
            # Return empty results on error
            return []