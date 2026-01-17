"""
Utilitaire pour exécuter des commandes système de manière sécurisée
"""
import subprocess
import os
import time
from typing import Dict, Optional

class CommandExecutor:
    """
    Exécute des commandes système avec timeout et capture des logs
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
    
    def execute(
        self, 
        command: str, 
        cwd: Optional[str] = None,
        timeout: int = 300,
        env: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Exécute une commande et retourne le résultat
        
        Args:
            command: Commande à exécuter
            cwd: Répertoire de travail (défaut: project_root)
            timeout: Timeout en secondes (défaut: 300s = 5min)
            env: Variables d'environnement additionnelles
            
        Returns:
            Dict avec success, exit_code, stdout, stderr, duration
        """
        if cwd is None:
            cwd = self.project_root
        
        # Vérifier que cwd est dans project_root (sécurité)
        if not os.path.abspath(cwd).startswith(os.path.abspath(self.project_root)):
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": "Error: cwd must be within project root",
                "duration": 0
            }
        
        # Préparer environnement
        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)
        
        start_time = time.time()
        
        try:
            # Exécuter commande
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                env=exec_env,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            duration = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration": round(duration, 2)
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout}s",
                "duration": round(duration, 2)
            }
            
        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "duration": round(duration, 2)
            }
