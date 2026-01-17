"""
Middleware d'authentification pour CASCADE API
Vérifie l'API Key dans le header Authorization
"""
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

CASCADE_API_KEY = os.getenv("CASCADE_API_KEY")

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Vérifie que l'API Key est valide
    """
    if credentials.credentials != CASCADE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return credentials.credentials
