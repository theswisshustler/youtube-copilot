"""
API REST pour le Générateur de Titres YouTube
Créé avec FastAPI pour être utilisé avec n8n et autres outils d'automatisation
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv

from youtube_api import get_transcript_from_url
from title_generator import generate_titles

# Charger les variables d'environnement
load_dotenv()

# Créer l'application FastAPI
app = FastAPI(
    title="YouTube Title Generator API",
    description="API pour générer des titres YouTube optimisés avec Claude AI",
    version="1.0.0"
)

# Configurer CORS pour permettre les requêtes depuis n'importe où
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modèles de données
class GenerateTitlesRequest(BaseModel):
    youtube_url: str = Field(..., description="URL complète de la vidéo YouTube")
    num_titles: int = Field(default=5, ge=1, le=10, description="Nombre de titres à générer (1-10)")

    class Config:
        json_schema_extra = {
            "example": {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "num_titles": 5
            }
        }


class GenerateTitlesResponse(BaseModel):
    success: bool
    titles: Optional[List[str]] = None
    analysis: Optional[str] = None
    error: Optional[str] = None
    transcript_length: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "titles": [
                    "🔥 Top 5 des astuces que PERSONNE ne connaît !",
                    "Comment gagner 1000€/mois avec cette méthode simple",
                    "Le secret pour réussir en 2024 (révélé)"
                ],
                "analysis": "Analyse Word Balance et scores...",
                "transcript_length": 15430,
                "error": None
            }
        }


class HealthResponse(BaseModel):
    status: str
    message: str


# Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """Route racine - Vérifie que l'API fonctionne"""
    return {
        "status": "ok",
        "message": "YouTube Title Generator API est en ligne ! Utilisez /docs pour voir la documentation."
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Vérification de santé de l'API"""
    # Vérifier que la clé API Anthropic est configurée
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Clé API Anthropic non configurée. Configurez ANTHROPIC_API_KEY dans les variables d'environnement."
        )

    return {
        "status": "healthy",
        "message": "API configurée et prête à générer des titres"
    }


@app.post("/generate-titles", response_model=GenerateTitlesResponse)
async def generate_youtube_titles(request: GenerateTitlesRequest):
    """
    Génère des titres optimisés pour une vidéo YouTube

    - **youtube_url**: URL complète de la vidéo YouTube
    - **num_titles**: Nombre de titres à générer (1-10, défaut: 5)

    Retourne une liste de titres optimisés pour maximiser les vues
    """
    # Vérifier la clé API Anthropic
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise HTTPException(
            status_code=500,
            detail="Clé API Anthropic non configurée"
        )

    try:
        # Étape 1: Récupérer la transcription
        transcript, error = get_transcript_from_url(request.youtube_url)

        if not transcript:
            return GenerateTitlesResponse(
                success=False,
                titles=None,
                error=error or "Impossible de récupérer la transcription",
                transcript_length=None
            )

        # Étape 2: Générer les titres
        result = generate_titles(
            transcript,
            anthropic_api_key,
            num_titles=request.num_titles
        )

        titles = result.get("titles", [])
        raw_response = result.get("raw_response", "")

        if not titles:
            return GenerateTitlesResponse(
                success=False,
                titles=None,
                analysis=None,
                error="Impossible de générer les titres avec Claude AI",
                transcript_length=len(transcript)
            )

        # Succès !
        return GenerateTitlesResponse(
            success=True,
            titles=titles,
            analysis=raw_response if raw_response else None,
            error=None,
            transcript_length=len(transcript)
        )

    except Exception as e:
        # Gérer les erreurs inattendues
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne: {str(e)}"
        )


# Point d'entrée pour le développement local
if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🚀 Démarrage de l'API YouTube Title Generator")
    print("=" * 60)
    print()
    print("📖 Documentation interactive: http://localhost:8000/docs")
    print("🔍 Santé de l'API: http://localhost:8000/health")
    print()
    print("Appuyez sur CTRL+C pour arrêter")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000)
