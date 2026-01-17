"""
Gestionnaire Git pour CASCADE API
Commit, push, status
"""
import os
from git import Repo, GitCommandError
from typing import List, Optional

class GitManager:
    """
    Gère les opérations Git
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        try:
            self.repo = Repo(project_root)
        except Exception as e:
            raise ValueError(f"Invalid git repository: {e}")
    
    def commit(
        self, 
        message: str, 
        files: Optional[List[str]] = None,
        push: bool = False
    ) -> dict:
        """
        Commit des fichiers avec message
        
        Args:
            message: Message de commit
            files: Liste de fichiers à commiter (None = tous les modifiés)
            push: Push après commit
            
        Returns:
            Dict avec success, commit_hash, pushed
        """
        try:
            # Ajouter fichiers
            if files:
                self.repo.index.add(files)
            else:
                self.repo.git.add(A=True)
            
            # Vérifier s'il y a des changements
            if not self.repo.index.diff("HEAD"):
                return {
                    "success": False,
                    "error": "No changes to commit"
                }
            
            # Commit
            commit = self.repo.index.commit(message)
            commit_hash = commit.hexsha[:7]
            
            result = {
                "success": True,
                "commit_hash": commit_hash,
                "message": message,
                "pushed": False
            }
            
            # Push si demandé
            if push:
                try:
                    origin = self.repo.remote('origin')
                    origin.push()
                    result["pushed"] = True
                except GitCommandError as e:
                    result["push_error"] = str(e)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def status(self) -> dict:
        """
        Retourne le statut Git
        
        Returns:
            Dict avec branch, modified, untracked, ahead, behind
        """
        try:
            # Branch actuelle
            branch = self.repo.active_branch.name
            
            # Fichiers modifiés
            modified = [item.a_path for item in self.repo.index.diff(None)]
            
            # Fichiers non trackés
            untracked = self.repo.untracked_files
            
            # Commits ahead/behind
            try:
                ahead = len(list(self.repo.iter_commits('origin/main..HEAD')))
                behind = len(list(self.repo.iter_commits('HEAD..origin/main')))
            except:
                ahead = 0
                behind = 0
            
            return {
                "success": True,
                "branch": branch,
                "modified": modified,
                "untracked": untracked,
                "ahead": ahead,
                "behind": behind
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
