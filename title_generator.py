"""
Module pour générer des titres YouTube avec l'IA Claude (Anthropic)
"""
from anthropic import Anthropic
from typing import List


def generate_titles(transcript: str, api_key: str, num_titles: int = 5) -> List[str]:
    """
    Génère des propositions de titres YouTube à partir d'une transcription.

    Args:
        transcript: La transcription complète de la vidéo
        api_key: Votre clé API Anthropic
        num_titles: Nombre de titres à générer (par défaut 5)

    Returns:
        Liste de titres proposés
    """
    print(f"🤖 Analyse de la transcription avec Claude...")

    # Initialiser le client Anthropic
    client = Anthropic(api_key=api_key)

    # Construire le prompt pour Claude
    prompt = f"""Analyse cette transcription de vidéo YouTube et génère {num_titles} propositions de titres optimisés.

Les titres doivent être :
- Accrocheurs et engageants
- Clairs sur le contenu de la vidéo
- Optimisés pour le référencement YouTube
- Entre 40 et 70 caractères idéalement
- En français

Transcription :
{transcript[:3000]}...

Réponds UNIQUEMENT avec les {num_titles} titres, un par ligne, numérotés de 1 à {num_titles}."""

    try:
        # Appeler l'API Claude avec le modèle Sonnet 4.5 (février 2026)
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extraire la réponse
        response_text = message.content[0].text

        # Parser les titres (un par ligne)
        titles = []
        for line in response_text.strip().split('\n'):
            line = line.strip()
            if line and len(line) > 0:
                # Retirer les numéros au début (1., 2., etc.)
                cleaned_title = re.sub(r'^\d+[\.\)]\s*', '', line)
                if cleaned_title:
                    titles.append(cleaned_title)

        return titles[:num_titles]

    except Exception as e:
        print(f"❌ Erreur lors de la génération des titres: {e}")
        return []


import re
