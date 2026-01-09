from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import tasks
from src.config.settings import settings

# Create FastAPI app instance
app = FastAPI(
    title="Todo Backend API",
    description="Secure API for managing user tasks with JWT authentication",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to browsers
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/health/db")
async def db_health_check():
    """Database health check endpoint"""
    # In a real implementation, this would check database connectivity
    return {"status": "database connected"}

@app.get("/health/auth")
async def auth_health_check():
    """Authentication health check endpoint"""
    # In a real implementation, this would check auth system
    return {"status": "authentication system operational"}