"""
Module pour récupérer les transcriptions YouTube via l'API youtube-transcript.io
API fiable et rapide qui fonctionne partout (y compris Streamlit Cloud)
"""
import sys
import requests
import re
from typing import Optional
import time
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'encodage UTF-8 pour Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    try:
        import io
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass


def extract_video_id(youtube_url: str) -> Optional[str]:
    """
    Extrait l'ID d'une vidéo YouTube depuis son URL.

    Exemples d'URLs supportées :
    - https://www.youtube.com/watch?v=dQw4w9WgXcQ
    - https://youtu.be/dQw4w9WgXcQ
    - https://www.youtube.com/embed/dQw4w9WgXcQ

    Args:
        youtube_url: L'URL complète de la vidéo YouTube

    Returns:
        L'ID de la vidéo ou None si l'URL est invalide
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*?v=([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    return None


def get_transcript(video_id: str, api_token: Optional[str] = None, retries: int = 3) -> tuple[Optional[str], Optional[str]]:
    """
    Récupère la transcription d'une vidéo YouTube via l'API youtube-transcript.io
    API fiable qui fonctionne partout, y compris sur Streamlit Cloud

    Args:
        video_id: L'ID de la vidéo YouTube
        api_token: Token API youtube-transcript.io (ou None pour utiliser l'env var)
        retries: Nombre de tentatives en cas d'échec

    Returns:
        Un tuple (transcription, erreur) - transcription est le texte ou None,
        erreur est le message d'erreur ou None si succès
    """
    # Récupérer le token API
    if not api_token:
        api_token = os.getenv("YOUTUBE_TRANSCRIPT_API_KEY")

    if not api_token:
        return None, "Token API youtube-transcript.io non configuré. Configurez YOUTUBE_TRANSCRIPT_API_KEY dans .env"

    # URL de l'API
    api_url = "https://www.youtube-transcript.io/api/transcripts"

    last_error = None

    for attempt in range(retries):
        try:
            # Préparer la requête
            headers = {
                "Authorization": f"Basic {api_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "ids": [video_id]
            }

            # Faire la requête
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            # Gérer les erreurs HTTP
            if response.status_code == 401:
                return None, "Token API invalide. Vérifiez votre YOUTUBE_TRANSCRIPT_API_TOKEN dans .env"

            elif response.status_code == 429:
                # Rate limit dépassé
                retry_after = response.headers.get('Retry-After', '10')
                if attempt < retries - 1:
                    time.sleep(int(retry_after))
                    continue
                return None, f"Trop de requêtes. Réessayez dans {retry_after} secondes."

            elif response.status_code == 404:
                return None, "Vidéo introuvable ou transcription non disponible."

            elif response.status_code != 200:
                last_error = f"Erreur HTTP {response.status_code}: {response.text}"
                if attempt < retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                return None, last_error

            # Parser la réponse JSON
            data = response.json()

            # L'API retourne un array avec un objet pour chaque video ID
            if not data or len(data) == 0:
                return None, "Aucune transcription trouvée pour cette vidéo."

            video_data = data[0]

            # Vérifier s'il y a une erreur
            if "error" in video_data:
                return None, f"Erreur API: {video_data['error']}"

            # L'API retourne la transcription de deux façons :
            # 1. Un champ "text" avec la transcription complète (simple)
            # 2. Un champ "tracks" avec les segments détaillés (avec timestamps)

            # Méthode 1 : Utiliser le champ "text" (plus simple et direct)
            if "text" in video_data and video_data["text"]:
                full_text = video_data["text"]
                return full_text, None

            # Méthode 2 : Si "text" n'existe pas, utiliser "tracks"
            if "tracks" in video_data and len(video_data["tracks"]) > 0:
                # Prendre le premier track (généralement en anglais ou langue principale)
                track = video_data["tracks"][0]
                if "transcript" in track:
                    transcript_entries = track["transcript"]
                    # Combiner tous les segments
                    full_text = " ".join([entry.get("text", "") for entry in transcript_entries])
                    if full_text.strip():
                        return full_text, None

            # Si aucune méthode ne fonctionne
            return None, "Transcription non disponible pour cette vidéo."

        except requests.exceptions.Timeout:
            last_error = "Timeout: La requête a pris trop de temps."
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue

        except requests.exceptions.ConnectionError:
            last_error = "Erreur de connexion à l'API youtube-transcript.io"
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue

        except requests.exceptions.RequestException as e:
            last_error = f"Erreur de requête: {str(e)}"
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue

        except (KeyError, ValueError, TypeError) as e:
            last_error = f"Erreur de parsing de la réponse: {str(e)}"
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue

        except Exception as e:
            last_error = f"Erreur inattendue: {str(e)}"
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue

    # Si on arrive ici, toutes les tentatives ont échoué
    if last_error:
        return None, f"Échec après {retries} tentatives: {last_error}"
    return None, "Impossible de récupérer la transcription."


def get_transcript_from_url(youtube_url: str) -> tuple[Optional[str], Optional[str]]:
    """
    Fonction combinée : extrait l'ID et récupère la transcription en une seule étape.

    Args:
        youtube_url: L'URL complète de la vidéo YouTube

    Returns:
        Un tuple (transcription, erreur) - transcription est le texte ou None,
        erreur est le message d'erreur ou None si succès
    """
    print(f"🔍 Extraction de l'ID de la vidéo...")
    video_id = extract_video_id(youtube_url)

    if not video_id:
        error_msg = "URL YouTube invalide. Formats acceptés: youtube.com/watch?v=..., youtu.be/..., youtube.com/embed/..."
        print(f"❌ {error_msg}")
        return None, error_msg

    print(f"✅ ID trouvé: {video_id}")
    print(f"📥 Récupération de la transcription...")

    transcript, error = get_transcript(video_id)

    if transcript:
        print(f"✅ Transcription récupérée ({len(transcript)} caractères)")
    elif error:
        print(f"❌ {error}")

    return transcript, error
