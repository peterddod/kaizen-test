import httpx
import base64
from typing import List, Dict
from config import settings

class DataForSEOService:
    def __init__(self):
        self.base_url = "https://api.dataforseo.com/v3"
        credentials = f"{settings.DATAFORSEO_LOGIN}:{settings.DATAFORSEO_PASSWORD}"
        self.auth_header = base64.b64encode(credentials.encode()).decode()
    
    async def get_serp_results(self, keyword: str, location: str = "Ireland") -> List[Dict]:
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
        
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, json=payload, headers=headers)
            
        if response.status_code == 200:
            data = response.json()
            results = []
            
            if data["tasks"] and data["tasks"][0]["result"]:
                items = data["tasks"][0]["result"][0]["items"][:10]
                
                for idx, item in enumerate(items):
                    if item.get("type") == "organic":
                        results.append({
                            "position": idx + 1,
                            "url": item.get("url", ""),
                            "title": item.get("title", ""),
                            "description": item.get("description", "")
                        })
            
            return results
        else:
            raise Exception(f"DataForSEO API error: {response.status_code}")