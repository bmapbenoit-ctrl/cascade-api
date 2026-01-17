"""
Router pour les opérations Git
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv

from middleware.auth import verify_api_key
from utils.git_manager import GitManager

load_dotenv()

router = APIRouter(prefix="/api", tags=["git"])

PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/Users/planetebeauty/Documents/copilote-planetebeauty")
git_manager = GitManager(PROJECT_ROOT)

class GitCommitRequest(BaseModel):
    message: str
    files: Optional[List[str]] = None
    push: bool = False

@router.post("/git_commit")
async def git_commit(
    request: GitCommitRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Commit des fichiers avec message
    
    Args:
        message: Message de commit
        files: Liste de fichiers à commiter (None = tous)
        push: Push après commit
        
    Returns:
        Résultat du commit
    """
    result = git_manager.commit(
        message=request.message,
        files=request.files,
        push=request.push
    )
    
    return result

@router.get("/git_status")
async def git_status(api_key: str = Depends(verify_api_key)):
    """
    Retourne le statut Git
    
    Returns:
        Statut Git (branch, modified, untracked, ahead, behind)
    """
    result = git_manager.status()
    
    return result
