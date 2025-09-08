from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import LandingPageRequest, AnalysisResponse
from services.openai_service import generate_keywords
from services.dataforseo_service import DataForSEOService

router = APIRouter()
dataforseo = DataForSEOService()

@router.post("/analyse", response_model=AnalysisResponse)
async def analyse_landing_page(request: LandingPageRequest):
    try:
        # Generate keywords using OpenAI
        keywords = await generate_keywords(
            request.content,
            request.client_name,
            request.campaign_name
        )
        
        # Select first keyword for SERP analysis
        selected_keyword = keywords[0] if keywords else ""
        
        # Get SERP results for the selected keyword
        serp_results = await dataforseo.get_serp_results(selected_keyword)
        
        return AnalysisResponse(
            suggested_keywords=keywords,
            selected_keyword=selected_keyword,
            serp_results=serp_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyse-file")
async def analyse_file(
    file: UploadFile = File(...),
    client_name: str = "Chill.ie",
    campaign_name: str = None
):
    content = await file.read()
    text_content = content.decode('utf-8')
    
    request = LandingPageRequest(
        content=text_content,
        client_name=client_name,
        campaign_name=campaign_name
    )
    
    return await analyse_landing_page(request)