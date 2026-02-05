"""
Module pour générer des titres YouTube avec l'IA Claude (Anthropic)
"""
from anthropic import Anthropic
from typing import List, Optional, Dict, Any, Union
from pathlib import Path


def load_system_prompt() -> Optional[str]:
    """
    Charge le system prompt depuis le fichier de configuration.

    Returns:
        Le contenu du fichier prompts/system_prompt.txt ou None si absent
    """
    prompt_path = Path(__file__).parent / "prompts" / "system_prompt.txt"
    if prompt_path.exists():
        content = prompt_path.read_text(encoding="utf-8").strip()
        if content:
            return content
    return None


def generate_titles(transcript: str, api_key: str, num_titles: int = 5) -> Dict[str, Any]:
    """
    Génère des propositions de titres YouTube à partir d'une transcription.

    Args:
        transcript: La transcription complète de la vidéo
        api_key: Votre clé API Anthropic
        num_titles: Nombre de titres à générer (par défaut 5)

    Returns:
        Dict avec 'titles' (liste), 'raw_response' (texte complet), 'has_custom_prompt' (bool)
    """
    print(f"🤖 Analyse de la transcription avec Claude...")

    # Initialiser le client Anthropic
    client = Anthropic(api_key=api_key)

    # Construire le prompt pour Claude
    # Si un system prompt personnalisé existe, on lui laisse contrôler le format
    system_prompt = load_system_prompt()

    if system_prompt:
        # Prompt simplifié - le system prompt gère les instructions
        prompt = f"""Génère {num_titles} titres optimisés pour cette vidéo YouTube.

Transcription :
{transcript[:3000]}..."""
    else:
        # Prompt complet par défaut (sans system prompt)
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
        api_params = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }

        # Ajouter le system prompt s'il existe
        if system_prompt:
            api_params["system"] = system_prompt
            print(f"📋 System prompt chargé ({len(system_prompt)} caractères)")

        message = client.messages.create(**api_params)

        # Extraire la réponse
        response_text = message.content[0].text

        # Parser les titres (lignes commençant par un numéro ou contenant "Titre")
        titles = []
        for line in response_text.strip().split('\n'):
            line = line.strip()
            # Chercher les lignes de titre (numérotées ou avec "Titre :")
            if re.match(r'^\d+[\.\)]\s*', line) or line.startswith('Titre'):
                # Retirer les préfixes
                cleaned = re.sub(r'^(Titre\s*:?\s*|\d+[\.\)]\s*)', '', line)
                # Retirer les guillemets
                cleaned = cleaned.strip('"\'""')
                if cleaned and len(cleaned) > 10:  # Titre minimum 10 chars
                    titles.append(cleaned)

        return {
            "titles": titles[:num_titles],
            "raw_response": response_text,
            "has_custom_prompt": system_prompt is not None
        }

    except Exception as e:
        print(f"❌ Erreur lors de la génération des titres: {e}")
        return {"titles": [], "raw_response": "", "has_custom_prompt": False}


import re


def generate_titles_from_description(description: str, api_key: str, num_titles: int = 5) -> Dict[str, Any]:
    """
    Génère des propositions de titres YouTube à partir d'une description.

    Args:
        description: Courte description du contenu de la vidéo
        api_key: Votre clé API Anthropic
        num_titles: Nombre de titres à générer (par défaut 5)

    Returns:
        Dict avec 'titles' (liste), 'raw_response' (texte complet), 'has_custom_prompt' (bool)
    """
    print(f"🤖 Génération de titres à partir de la description...")

    # Initialiser le client Anthropic
    client = Anthropic(api_key=api_key)

    # Charger le system prompt personnalisé
    system_prompt = load_system_prompt()

    if system_prompt:
        # Prompt simplifié - le system prompt gère les instructions
        prompt = f"""Génère {num_titles} titres optimisés pour une vidéo YouTube.

Description de la vidéo :
{description}"""
    else:
        # Prompt complet par défaut (sans system prompt)
        prompt = f"""Génère {num_titles} propositions de titres optimisés pour une vidéo YouTube.

Description de la vidéo :
{description}

Les titres doivent être :
- Accrocheurs et engageants
- Clairs sur le contenu de la vidéo
- Optimisés pour le référencement YouTube
- Entre 40 et 70 caractères idéalement
- En français

Réponds UNIQUEMENT avec les {num_titles} titres, un par ligne, numérotés de 1 à {num_titles}."""

    try:
        # Appeler l'API Claude
        api_params = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }

        # Ajouter le system prompt s'il existe
        if system_prompt:
            api_params["system"] = system_prompt
            print(f"📋 System prompt chargé ({len(system_prompt)} caractères)")

        message = client.messages.create(**api_params)

        # Extraire la réponse
        response_text = message.content[0].text

        # Parser les titres
        titles = []
        for line in response_text.strip().split('\n'):
            line = line.strip()
            if re.match(r'^\d+[\.\)]\s*', line) or line.startswith('Titre'):
                cleaned = re.sub(r'^(Titre\s*:?\s*|\d+[\.\)]\s*)', '', line)
                cleaned = cleaned.strip('"\'""')
                if cleaned and len(cleaned) > 10:
                    titles.append(cleaned)

        return {
            "titles": titles[:num_titles],
            "raw_response": response_text,
            "has_custom_prompt": system_prompt is not None
        }

    except Exception as e:
        print(f"❌ Erreur lors de la génération des titres: {e}")
        return {"titles": [], "raw_response": "", "has_custom_prompt": False}
