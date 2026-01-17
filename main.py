"""
CASCADE API - API pour permettre à STELLA MASTER d'exécuter des commandes
FastAPI application principale
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from routers import commands, files, git

load_dotenv()

app = FastAPI(
    title="CASCADE API",
    description="API pour permettre à STELLA MASTER d'exécuter des commandes de manière autonome",
    version="1.0.0"
)

# CORS (pour permettre les appels depuis Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production: spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(commands.router)
app.include_router(files.router)
app.include_router(git.router)

@app.get("/")
async def root():
    """
    Endpoint racine - Health check
    """
    return {
        "status": "online",
        "service": "CASCADE API",
        "version": "1.0.0",
        "endpoints": [
            "/api/execute_command",
            "/api/create_file",
            "/api/edit_file",
            "/api/read_file",
            "/api/git_commit",
            "/api/git_status"
        ]
    }

@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
