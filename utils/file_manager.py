"""
Gestionnaire de fichiers pour CASCADE API
Création, édition, lecture de fichiers de manière sécurisée
"""
import os
from typing import Optional

class FileManager:
    """
    Gère les opérations sur les fichiers
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
    
    def _validate_path(self, path: str) -> bool:
        """
        Vérifie que le chemin est dans project_root (sécurité)
        """
        abs_path = os.path.abspath(path)
        abs_root = os.path.abspath(self.project_root)
        return abs_path.startswith(abs_root)
    
    def create_file(self, path: str, content: str, overwrite: bool = False) -> dict:
        """
        Crée un fichier avec le contenu spécifié
        
        Args:
            path: Chemin du fichier
            content: Contenu du fichier
            overwrite: Autoriser l'écrasement si existe
            
        Returns:
            Dict avec success, path, size
        """
        if not self._validate_path(path):
            return {
                "success": False,
                "error": "Path must be within project root"
            }
        
        if os.path.exists(path) and not overwrite:
            return {
                "success": False,
                "error": "File already exists (use overwrite=true)"
            }
        
        try:
            # Créer répertoires parents si nécessaire
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Écrire fichier
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            size = os.path.getsize(path)
            
            return {
                "success": True,
                "path": path,
                "size": size
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def edit_file(self, path: str, old_string: str, new_string: str) -> dict:
        """
        Édite un fichier en remplaçant old_string par new_string
        
        Args:
            path: Chemin du fichier
            old_string: Chaîne à remplacer
            new_string: Nouvelle chaîne
            
        Returns:
            Dict avec success, changes
        """
        if not self._validate_path(path):
            return {
                "success": False,
                "error": "Path must be within project root"
            }
        
        if not os.path.exists(path):
            return {
                "success": False,
                "error": "File does not exist"
            }
        
        try:
            # Lire fichier
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Compter occurrences
            count = content.count(old_string)
            
            if count == 0:
                return {
                    "success": False,
                    "error": "String not found in file"
                }
            
            # Remplacer
            new_content = content.replace(old_string, new_string)
            
            # Écrire
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {
                "success": True,
                "changes": count,
                "path": path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def read_file(self, path: str) -> dict:
        """
        Lit le contenu d'un fichier
        
        Args:
            path: Chemin du fichier
            
        Returns:
            Dict avec success, content, size
        """
        if not self._validate_path(path):
            return {
                "success": False,
                "error": "Path must be within project root"
            }
        
        if not os.path.exists(path):
            return {
                "success": False,
                "error": "File does not exist"
            }
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            size = os.path.getsize(path)
            
            return {
                "success": True,
                "content": content,
                "size": size,
                "path": path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
