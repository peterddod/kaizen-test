from pydantic import BaseModel
from typing import List, Optional

class LandingPageRequest(BaseModel):
    content: str
    client_name: Optional[str] = "Chill.ie"
    campaign_name: Optional[str] = None
    campaign_url: Optional[str] = None
    
class KeywordSuggestion(BaseModel):
    keywords: List[str]
    
class SERPResult(BaseModel):
    position: int
    url: str
    title: str
    description: str

class AnalysisResponse(BaseModel):
    suggested_keywords: List[str]
    selected_keyword: str
    serp_results: List[SERPResult]