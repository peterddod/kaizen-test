import openai
from typing import List
from config import settings

openai.api_key = settings.OPENAI_API_KEY

async def generate_keywords(content: str, client_name: str, campaign_name: str = None) -> List[str]:
    prompt = f"""
    Analyze this landing page content and generate Google search keywords that journalists 
    and websites might use to find articles about this PR campaign.
    
    Client Name: {client_name}
    Campaign Name: {campaign_name if campaign_name else "Not specified"}
    
    Landing Page Content:
    {content}
    
    Generate keywords following these patterns:
    1. Campaign Name + Client Name
    2. Main topic/headline from content
    3. Key statistics or findings mentioned
    4. Location-specific searches if mentioned
    5. Industry-specific terms
    
    Return exactly 10 relevant search keywords as a comma-separated list.
    Focus on keywords that would help find news coverage of this campaign.
    """
    
    response = await openai.ChatCompletion.acreate(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are an SEO expert helping identify news coverage."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    keywords = response.choices[0].message.content.split(',')
    return [k.strip() for k in keywords]