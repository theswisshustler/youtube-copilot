"""
Module pour récupérer les transcriptions YouTube via youtube-transcript-api
Cette bibliothèque est gratuite et ne nécessite pas de clé API !
"""
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re
from typing import Optional

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


def get_transcript(video_id: str) -> Optional[str]:
    """
    Récupère la transcription d'une vidéo YouTube via youtube-transcript-api.
    Cette méthode est gratuite et ne nécessite pas de clé API !

    Args:
        video_id: L'ID de la vidéo YouTube

    Returns:
        La transcription complète de la vidéo ou None en cas d'erreur
    """
    try:
        # Créer une instance de l'API
        api = YouTubeTranscriptApi()

        # Essayer d'abord en français, puis anglais
        transcript_data = None

        try:
            transcript_data = api.fetch(video_id, languages=['fr'])
        except:
            try:
                transcript_data = api.fetch(video_id, languages=['en'])
            except:
                # Essayer avec la première langue disponible
                transcript_data = api.fetch(video_id, languages=['en', 'fr'])

        if not transcript_data:
            return None

        # Combiner tous les segments de texte depuis l'objet FetchedTranscript
        full_text = " ".join([snippet.text for snippet in transcript_data.snippets])
        return full_text

    except TranscriptsDisabled:
        print("❌ Les sous-titres sont désactivés pour cette vidéo.")
        return None

    except NoTranscriptFound:
        print("❌ Aucune transcription trouvée pour cette vidéo.")
        print("   La vidéo doit avoir des sous-titres (automatiques ou manuels).")
        return None

    except VideoUnavailable:
        print("❌ Vidéo introuvable ou indisponible.")
        return None

    except Exception as e:
        print(f"❌ Erreur lors de la récupération de la transcription: {e}")
        return None


def get_transcript_from_url(youtube_url: str) -> Optional[str]:
    """
    Fonction combinée : extrait l'ID et récupère la transcription en une seule étape.

    Args:
        youtube_url: L'URL complète de la vidéo YouTube

    Returns:
        La transcription complète ou None en cas d'erreur
    """
    print(f"🔍 Extraction de l'ID de la vidéo...")
    video_id = extract_video_id(youtube_url)

    if not video_id:
        print("❌ URL YouTube invalide. Vérifiez le format.")
        return None

    print(f"✅ ID trouvé: {video_id}")
    print(f"📥 Récupération de la transcription...")

    transcript = get_transcript(video_id)

    if transcript:
        print(f"✅ Transcription récupérée ({len(transcript)} caractères)")

    return transcript
