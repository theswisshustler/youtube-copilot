"""
Interface Web pour le Générateur de Titres YouTube
Lancez avec: streamlit run app_web.py
"""
import streamlit as st
import os
from dotenv import load_dotenv
from youtube_api import get_transcript_from_url
from title_generator import generate_titles

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Titres YouTube",
    page_icon="🎬",
    layout="wide"
)

# Charger les variables d'environnement
load_dotenv()

# Titre de l'application
st.title("🎬 Générateur de Titres YouTube")
st.markdown("---")

# Vérifier la clé API (supporte .env local ET Streamlit Cloud secrets)
try:
    # Essayer d'abord les secrets Streamlit Cloud
    anthropic_api_key = st.secrets.get("ANTHROPIC_API_KEY")
    youtube_api_token = st.secrets.get("YOUTUBE_TRANSCRIPT_API_TOKEN")
except (FileNotFoundError, KeyError):
    # Fallback sur .env pour développement local
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    youtube_api_token = os.getenv("YOUTUBE_TRANSCRIPT_API_TOKEN")

if not anthropic_api_key:
    st.error("❌ Clé API Anthropic non configurée. Configurez ANTHROPIC_API_KEY dans les secrets Streamlit ou dans le fichier .env")
    st.stop()

# Interface utilisateur
col1, col2 = st.columns([2, 1])

with col1:
    youtube_url = st.text_input(
        "🔗 Lien de la vidéo YouTube",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Collez l'URL complète de votre vidéo YouTube"
    )

with col2:
    num_titles = st.slider(
        "📊 Nombre de titres",
        min_value=1,
        max_value=10,
        value=5,
        help="Choisissez combien de titres vous voulez générer"
    )

# Bouton de génération
if st.button("✨ Générer les titres", type="primary", use_container_width=True):
    if not youtube_url:
        st.warning("⚠️ Veuillez entrer une URL YouTube")
    else:
        # Barre de progression
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Étape 1: Récupération de la transcription
        status_text.text("📝 Récupération de la transcription...")
        progress_bar.progress(30)

        with st.spinner("Extraction de la transcription..."):
            transcript, error = get_transcript_from_url(youtube_url)

        if not transcript:
            st.error(f"❌ {error or 'Impossible de récupérer la transcription.'}")
            st.stop()

        # Étape 2: Génération des titres
        status_text.text("🤖 Génération des titres avec Claude...")
        progress_bar.progress(60)

        with st.spinner("Analyse par l'IA..."):
            titles = generate_titles(transcript, anthropic_api_key, num_titles=num_titles)

        progress_bar.progress(100)
        status_text.empty()

        if titles:
            st.success(f"✅ {len(titles)} titres générés avec succès!")
            st.markdown("---")

            # Affichage des titres
            st.subheader("🎯 Propositions de titres")

            for i, title in enumerate(titles, 1):
                col_title, col_copy = st.columns([5, 1])
                with col_title:
                    st.markdown(f"**{i}.** {title}")
                with col_copy:
                    if st.button("📋", key=f"copy_{i}", help="Copier ce titre"):
                        st.toast(f"✓ Titre {i} copié!", icon="✅")

            # Statistiques
            st.markdown("---")
            with st.expander("📊 Statistiques de la transcription"):
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Caractères", f"{len(transcript):,}")
                with col_stat2:
                    st.metric("Mots", f"{len(transcript.split()):,}")
                with col_stat3:
                    avg_title_len = sum(len(t) for t in titles) // len(titles)
                    st.metric("Longueur moy. titre", f"{avg_title_len} car.")
        else:
            st.error("❌ Impossible de générer les titres. Vérifiez votre clé API.")

# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ Information")
    st.markdown("""
    ### Comment utiliser
    1. Collez le lien d'une vidéo YouTube
    2. Choisissez le nombre de titres
    3. Cliquez sur "Générer"

    ### Prérequis
    - La vidéo doit avoir des sous-titres (automatiques ou manuels)
    - Clé API Anthropic configurée

    ### Fonctionnalités
    - ✅ Récupération gratuite des transcriptions
    - ✅ Génération IA avec Claude Sonnet 4.5
    - ✅ Titres optimisés SEO
    - ✅ Interface moderne et intuitive
    """)

    st.markdown("---")
    st.caption("🤖 Propulsé par Claude AI")
