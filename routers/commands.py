"""
Router pour l'exécution de commandes système
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, Dict
import os
from dotenv import load_dotenv

from middleware.auth import verify_api_key
from utils.executor import CommandExecutor

load_dotenv()

router = APIRouter(prefix="/api", tags=["commands"])

PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/Users/planetebeauty/Documents/copilote-planetebeauty")
executor = CommandExecutor(PROJECT_ROOT)

class ExecuteCommandRequest(BaseModel):
    command: str
    cwd: Optional[str] = None
    timeout: int = 300
    env: Optional[Dict[str, str]] = None

class ExecuteCommandResponse(BaseModel):
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    duration: float

@router.post("/execute_command", response_model=ExecuteCommandResponse)
async def execute_command(
    request: ExecuteCommandRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Exécute une commande système
    
    Args:
        command: Commande à exécuter
        cwd: Répertoire de travail (optionnel)
        timeout: Timeout en secondes (défaut: 300)
        env: Variables d'environnement additionnelles
        
    Returns:
        Résultat de l'exécution avec stdout, stderr, exit_code
    """
    result = executor.execute(
        command=request.command,
        cwd=request.cwd,
        timeout=request.timeout,
        env=request.env
    )
    
    return ExecuteCommandResponse(**result)
