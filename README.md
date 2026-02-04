# 🎬 Employé Virtuel - Générateur de Titres YouTube

Un assistant intelligent qui analyse vos vidéos YouTube et génère des titres accrocheurs en utilisant l'IA Claude.

## 📋 Prérequis

- Python 3.11 ou supérieur
- Un compte sur [youtube-transcript.io](https://www.youtube-transcript.io/) (pour obtenir les transcriptions)
- Une clé API Anthropic Claude (depuis [console.anthropic.com](https://console.anthropic.com/))

## 🚀 Installation

### 1. Installer Python

Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
**Important** : Cochez "Add Python to PATH" lors de l'installation !

### 2. Configurer le projet

Ouvrez un terminal dans le dossier du projet et exécutez :

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configurer les clés API

1. Copiez le fichier `.env.example` en `.env`
2. Ouvrez `.env` et ajoutez vos clés API :
   - Clé YouTube Transcript : créez un compte sur youtube-transcript.io et générez un token
   - Clé Anthropic : créez un compte sur console.anthropic.com

## 💡 Utilisation

```bash
python main.py
```

Le programme vous demandera :
1. Le lien de votre vidéo YouTube
2. Générera automatiquement 5 propositions de titres optimisés

## 📁 Structure du projet

- `main.py` : Script principal
- `youtube_api.py` : Gestion de l'API YouTube Transcript
- `title_generator.py` : Génération de titres avec Claude
- `requirements.txt` : Liste des bibliothèques Python
- `.env` : Vos clés API (à créer)

## ❓ Besoin d'aide ?

Si vous rencontrez des problèmes, vérifiez que :
- Python est bien installé (`python --version`)
- L'environnement virtuel est activé
- Les clés API sont correctement configurées dans `.env`
