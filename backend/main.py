import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.endpoints import query_api, table_structure_api
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


load_dotenv()

app = FastAPI(title="Health Fitness Tracker Backend")

frontend_url = os.getenv("FRONTEND_URL")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # Use the frontend URL from the environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(query_api.router, prefix="/query", tags=["Query API"])
app.include_router(table_structure_api.router, prefix="/tables", tags=["Table Structure API"])
