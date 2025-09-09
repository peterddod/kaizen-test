from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from models.schemas import LandingPageRequest, AnalysisResponse
from services.openai_service import generate_keywords
from services.dataforseo_service import DataForSEOService
import docx
from io import BytesIO
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
dataforseo = DataForSEOService()

@router.post("/analyse", response_model=AnalysisResponse)
async def analyse_landing_page(request: LandingPageRequest):
    try:
        logger.info(f"Analysing content for client: {request.client_name}")
        
        # Generate keywords using OpenAI
        keywords = await generate_keywords(
            request.content,
            request.client_name,
            request.campaign_name,
            request.campaign_url
        )
        
        logger.info(f"Generated {len(keywords)} keywords")
        
        # Select first keyword for SERP analysis
        selected_keyword = keywords[0] if keywords else ""
        
        logger.info(f"Fetching SERP results for keyword: {selected_keyword}")
        
        # Get SERP results for the selected keyword
        serp_results = await dataforseo.get_serp_results(selected_keyword)
        
        logger.info(f"Found {len(serp_results)} SERP results")
        
        return AnalysisResponse(
            suggested_keywords=keywords,
            selected_keyword=selected_keyword,
            serp_results=serp_results
        )
    except Exception as e:
        logger.error(f"Error in analyse_landing_page: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyse-file")
async def analyse_file(
    file: UploadFile = File(...),
    client_name: Optional[str] = Form(default="Chill.ie"),
    campaign_name: Optional[str] = Form(default=None),
    campaign_url: Optional[str] = Form(default=None)
):
    try:
        logger.info(f"Processing file: {file.filename}")
        logger.info(f"File content type: {file.content_type}")
        
        content = await file.read()
        logger.info(f"File size: {len(content)} bytes")
        
        # Check file type and extract text accordingly
        if file.filename.endswith('.docx'):
            logger.info("Processing as DOCX file")
            try:
                doc = docx.Document(BytesIO(content))
                paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
                text_content = '\n'.join(paragraphs)
                logger.info(f"Extracted {len(paragraphs)} paragraphs from DOCX")
            except Exception as docx_error:
                logger.error(f"Error reading DOCX: {str(docx_error)}")
                raise HTTPException(status_code=400, detail=f"Error reading DOCX file: {str(docx_error)}")
                
        elif file.filename.endswith(('.txt', '.text')):
            logger.info("Processing as text file")
            text_content = content.decode('utf-8')
        else:
            # Try to decode as text for other file types
            try:
                logger.info("Attempting to decode as UTF-8 text")
                text_content = content.decode('utf-8')
            except UnicodeDecodeError as decode_error:
                logger.error(f"Failed to decode file: {str(decode_error)}")
                raise HTTPException(status_code=400, detail="Unable to read file content. Please upload a .txt or .docx file.")
        
        if not text_content.strip():
            logger.warning("File appears to be empty")
            raise HTTPException(status_code=400, detail="The uploaded file appears to be empty.")
        
        logger.info(f"Text content length: {len(text_content)} characters")
        
        # Create request object
        request = LandingPageRequest(
            content=text_content,
            client_name=client_name,
            campaign_name=campaign_name,
            campaign_url=campaign_url
        )
        
        # Call the analyse function
        return await analyse_landing_page(request)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyse_file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")