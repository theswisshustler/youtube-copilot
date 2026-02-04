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


def get_transcript(video_id: str) -> tuple[Optional[str], Optional[str]]:
    """
    Récupère la transcription d'une vidéo YouTube via youtube-transcript-api.
    Cette méthode est gratuite et ne nécessite pas de clé API !

    Args:
        video_id: L'ID de la vidéo YouTube

    Returns:
        Un tuple (transcription, erreur) - transcription est le texte ou None,
        erreur est le message d'erreur ou None si succès
    """
    try:
        # Créer une instance de l'API
        api = YouTubeTranscriptApi()

        # Essayer d'abord en français, puis anglais, puis n'importe quelle langue
        transcript_data = None

        # Priorité : français
        try:
            transcript_data = api.fetch(video_id, languages=['fr'])
        except (NoTranscriptFound, Exception):
            pass

        # Fallback : anglais
        if not transcript_data:
            try:
                transcript_data = api.fetch(video_id, languages=['en'])
            except (NoTranscriptFound, Exception):
                pass

        # Fallback : n'importe quelle langue disponible
        if not transcript_data:
            try:
                transcript_list = api.list_transcripts(video_id)
                # Prendre la première transcription disponible
                for transcript in transcript_list:
                    transcript_data = transcript.fetch()
                    break
            except Exception:
                pass

        if not transcript_data:
            return None, "Aucune transcription disponible pour cette vidéo (ni sous-titres manuels, ni automatiques)."

        # Combiner tous les segments de texte depuis l'objet FetchedTranscript
        full_text = " ".join([snippet.text for snippet in transcript_data.snippets])
        return full_text, None

    except TranscriptsDisabled:
        return None, "Les sous-titres sont désactivés pour cette vidéo."

    except NoTranscriptFound:
        return None, "Aucune transcription trouvée. La vidéo doit avoir des sous-titres (automatiques ou manuels)."

    except VideoUnavailable:
        return None, "Vidéo introuvable ou indisponible (supprimée, privée ou bloquée dans votre région)."

    except Exception as e:
        error_msg = str(e)
        # Gérer les erreurs courantes de manière plus explicite
        if "Too Many Requests" in error_msg or "429" in error_msg:
            return None, "Trop de requêtes. Veuillez réessayer dans quelques minutes."
        if "Sign in" in error_msg or "age" in error_msg.lower():
            return None, "Cette vidéo nécessite une connexion YouTube (restriction d'âge ou contenu réservé)."
        return None, f"Erreur lors de la récupération: {error_msg}"


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
