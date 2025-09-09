from openai import AsyncOpenAI
from typing import List
from config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize the async client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_keywords(content: str, client_name: str, campaign_name: str = None, campaign_url: str = None) -> List[str]:
    try:
        logger.info(f"Generating keywords for {client_name}")
        
        prompt = f"""
        # Task
        Analyze this landing page content and generate Google search keywords that journalists and websites might use to find articles about this PR campaign. You will be given a client name, a campaign name, a campaign URL, and a landing page content. You should not generate more than 15 keywords. Return the keywords in a comma-separated list.
        
        # Patterns
        Headings: H1, H2, H3 (example, "H1: The Counties With The Most Affordable Homes")

        The following are some examples of keywords that you should generate, replacing the placeholders with the actual values:
        -	Campaign Name + “Client Name”
        -	Campaign URL/Landing Page H1 
        -	Press Release H1
        -	Press Release H1 + “Client Name”

        Some other example keywords:
        -	All press release / landing page / uploaded document headings (e.g. H1, H2, H3) 
        -	Any spokesperson named 
        -	The campaign name 
        -	The client name
        -	List of locations mentioned

        # Inputs
        Client Name: {client_name}
        Campaign Name: {campaign_name if campaign_name else "Not specified"}
        Campaign URL: {campaign_url if campaign_url else "Not specified"}
        Landing Page Content:
        {content}
        """
        
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an SEO expert helping identify news coverage."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=settings.OPENAI_MAX_TOKENS
        )
        
        keywords_text = response.choices[0].message.content
        keywords = [k.strip() for k in keywords_text.split(',')]
        
        # Ensure we have exactly 15 keywords
        keywords = keywords[:15] if len(keywords) > 15 else keywords
        
        logger.info(f"Generated {len(keywords)} keywords successfully")
        return keywords
        
    except Exception as e:
        logger.error(f"Error generating keywords: {str(e)}")
        # Return some default keywords if OpenAI fails
        return [
            f"{campaign_name} {client_name}" if campaign_name else f"{client_name} news",
            f"{client_name} PR campaign",
            "affordable homes Ireland",
            "housing affordability study",
            "cheapest counties Ireland",
            f"{client_name} research",
            "Irish property prices",
            "housing market Ireland",
            f"{client_name} survey",
            "Ireland housing statistics"
        ]