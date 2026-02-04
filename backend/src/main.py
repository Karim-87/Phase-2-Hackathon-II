from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import tasks
from app.routers import auth
from app.config import settings
app = FastAPI(
    title="Todo Backend API",
    # ... your other params ...
)

# CORS - MUST be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Temporary wildcard for debugging (remove in production!)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],  # Cover your fetch headers
    expose_headers=["Content-Type", "Authorization"],  # If needed
    max_age=600,  # Cache preflight for 10 min
)

# Now include your routers
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
# app = FastAPI(
#     title="Todo Backend API",
#     description="Secure API for managing user tasks with JWT authentication",
#     version="1.0.0",
#     openapi_url="/api/openapi.json",
#     docs_url="/api/docs",
#     redoc_url="/api/redoc",
# )

# # CORS middleware ko SABSE PEHLE add karo (routes se pehle!)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,          # ["http://localhost:3000", "http://127.0.0.1:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Access-Control-Allow-Origin"],   # optional but helpful
# )

# # Ab routes include karo
# app.include_router(tasks.router, prefix="/api", tags=["tasks"])
# app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

# Health endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ... baaki code same







# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from src.api.v1 import tasks
# from src.api.v1 import auth
# from src.config.settings import settings

# # Create FastAPI app instance
# app = FastAPI(
#     title="Todo Backend API",
#     description="Secure API for managing user tasks with JWT authentication",
#     version="1.0.0",
#     openapi_url="/api/openapi.json",
#     docs_url="/api/docs",
#     redoc_url="/api/redoc",
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     # Expose the authorization header to browsers
#     expose_headers=["Access-Control-Allow-Origin"]
# )

# # Include API routes
# app.include_router(tasks.router, prefix="/api", tags=["tasks"])
# app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy"}

# @app.get("/health/db")
# async def db_health_check():
#     """Database health check endpoint"""
#     # In a real implementation, this would check database connectivity
#     return {"status": "database connected"}

# @app.get("/health/auth")
# async def auth_health_check():
#     """Authentication health check endpoint"""
#     # In a real implementation, this would check auth system
#     return {"status": "authentication system operational"}