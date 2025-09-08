from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analysis
from config import settings

app = FastAPI(title="Link Dive MVP API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    return {"message": "Link Dive MVP API is running"}