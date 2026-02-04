"""
Employé Virtuel - Générateur de Titres YouTube
Script principal
"""
import os
import sys
from dotenv import load_dotenv
from youtube_api import get_transcript_from_url
from title_generator import generate_titles

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


def main():
    """Fonction principale du programme"""
    print("=" * 60)
    print("🎬 EMPLOYÉ VIRTUEL - GÉNÉRATEUR DE TITRES YOUTUBE")
    print("=" * 60)
    print()

    # Charger les variables d'environnement depuis .env
    load_dotenv()

    # Récupérer la clé API Anthropic
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    # Vérifier que la clé est configurée
    if not anthropic_api_key or anthropic_api_key == "votre_cle_anthropic_ici":
        print("❌ Erreur : Clé API Anthropic non configurée !")
        print("   → Ajoutez votre clé dans le fichier .env")
        print("   → Obtenez votre clé sur : https://console.anthropic.com/")
        return

    print("✅ Clé API Anthropic configurée")
    print("ℹ️  La récupération des transcriptions YouTube est gratuite (pas de clé nécessaire)")
    print()

    # Demander l'URL de la vidéo YouTube
    youtube_url = input("🔗 Entrez le lien de votre vidéo YouTube : ").strip()
    print()

    if not youtube_url:
        print("❌ Aucune URL fournie. Au revoir !")
        return

    # Étape 1 : Récupérer la transcription
    print("📝 ÉTAPE 1/2 : Récupération de la transcription")
    print("-" * 60)
    transcript = get_transcript_from_url(youtube_url)

    if not transcript:
        print("❌ Impossible de récupérer la transcription.")
        print("   Vérifiez que :")
        print("   - L'URL est valide")
        print("   - La vidéo existe")
        print("   - Votre clé API est correcte")
        return

    print()

    # Étape 2 : Générer les titres
    print("✨ ÉTAPE 2/2 : Génération des titres")
    print("-" * 60)
    titles = generate_titles(transcript, anthropic_api_key, num_titles=5)

    if not titles:
        print("❌ Impossible de générer les titres.")
        return

    print()
    print("=" * 60)
    print("🎯 PROPOSITIONS DE TITRES POUR VOTRE VIDÉO")
    print("=" * 60)
    print()

    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")

    print()
    print("=" * 60)
    print("✅ Terminé ! Choisissez le titre qui vous convient le mieux.")
    print("=" * 60)


if __name__ == "__main__":
    main()
