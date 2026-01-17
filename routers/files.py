"""
Router pour la gestion des fichiers
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from middleware.auth import verify_api_key
from utils.file_manager import FileManager

load_dotenv()

router = APIRouter(prefix="/api", tags=["files"])

PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/Users/planetebeauty/Documents/copilote-planetebeauty")
file_manager = FileManager(PROJECT_ROOT)

class CreateFileRequest(BaseModel):
    path: str
    content: str
    overwrite: bool = False

class EditFileRequest(BaseModel):
    path: str
    old_string: str
    new_string: str

class ReadFileRequest(BaseModel):
    path: str

@router.post("/create_file")
async def create_file(
    request: CreateFileRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Crée un nouveau fichier
    
    Args:
        path: Chemin du fichier
        content: Contenu du fichier
        overwrite: Autoriser l'écrasement si existe
        
    Returns:
        Résultat de la création
    """
    result = file_manager.create_file(
        path=request.path,
        content=request.content,
        overwrite=request.overwrite
    )
    
    return result

@router.post("/edit_file")
async def edit_file(
    request: EditFileRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Édite un fichier existant
    
    Args:
        path: Chemin du fichier
        old_string: Chaîne à remplacer
        new_string: Nouvelle chaîne
        
    Returns:
        Résultat de l'édition
    """
    result = file_manager.edit_file(
        path=request.path,
        old_string=request.old_string,
        new_string=request.new_string
    )
    
    return result

@router.post("/read_file")
async def read_file(
    request: ReadFileRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Lit le contenu d'un fichier
    
    Args:
        path: Chemin du fichier
        
    Returns:
        Contenu du fichier
    """
    result = file_manager.read_file(path=request.path)
    
    return result
