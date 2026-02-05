"""
Interface Web pour le Générateur de Titres YouTube
Lancez avec: streamlit run app_web.py
"""
import streamlit as st
import os
from dotenv import load_dotenv
from youtube_api import get_transcript_from_url
from title_generator import generate_titles, generate_titles_from_description

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

# Vérifier les clés API (supporte .env local ET Streamlit Cloud secrets)
try:
    # Essayer d'abord les secrets Streamlit Cloud
    anthropic_api_key = st.secrets.get("ANTHROPIC_API_KEY")
    youtube_api_token = st.secrets.get("YOUTUBE_TRANSCRIPT_API_KEY")
except (FileNotFoundError, KeyError, AttributeError):
    # Fallback sur .env pour développement local
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    youtube_api_token = os.getenv("YOUTUBE_TRANSCRIPT_API_KEY")

# Vérification clé API Anthropic (obligatoire)
if not anthropic_api_key:
    st.error("❌ Clé API Anthropic non configurée. Configurez ANTHROPIC_API_KEY dans les secrets Streamlit ou dans le fichier .env")
    st.stop()

# Onglets pour choisir le mode
tab_url, tab_description = st.tabs(["🔗 Depuis une URL YouTube", "📝 Depuis une description"])

# ============ ONGLET URL ============
with tab_url:
    if not youtube_api_token:
        st.warning("⚠️ Token YouTube Transcript non configuré. Cette fonctionnalité nécessite YOUTUBE_TRANSCRIPT_API_KEY.")
        st.info("💡 Obtenez votre token gratuit sur: https://www.youtube-transcript.io/profile")
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            youtube_url = st.text_input(
                "🔗 Lien de la vidéo YouTube",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Collez l'URL complète de votre vidéo YouTube"
            )

        with col2:
            num_titles_url = st.slider(
                "📊 Nombre de titres",
                min_value=1,
                max_value=10,
                value=5,
                help="Choisissez combien de titres vous voulez générer",
                key="num_titles_url"
            )

        if st.button("✨ Générer les titres", type="primary", use_container_width=True, key="btn_url"):
            if not youtube_url:
                st.warning("⚠️ Veuillez entrer une URL YouTube")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("📝 Récupération de la transcription...")
                progress_bar.progress(30)

                with st.spinner("Extraction de la transcription..."):
                    transcript, error = get_transcript_from_url(youtube_url)

                if not transcript:
                    st.error(f"❌ {error or 'Impossible de récupérer la transcription.'}")
                    st.stop()

                status_text.text("🤖 Génération des titres avec Claude...")
                progress_bar.progress(60)

                with st.spinner("Analyse par l'IA..."):
                    result = generate_titles(transcript, anthropic_api_key, num_titles=num_titles_url)

                progress_bar.progress(100)
                status_text.empty()

                titles = result.get("titles", [])
                raw_response = result.get("raw_response", "")
                has_custom_prompt = result.get("has_custom_prompt", False)

                if titles:
                    st.success(f"✅ {len(titles)} titres générés avec succès!")
                    st.markdown("---")

                    if has_custom_prompt and raw_response:
                        st.subheader("🎯 Analyse complète des titres")
                        st.markdown(raw_response)
                    else:
                        st.subheader("🎯 Propositions de titres")
                        for i, title in enumerate(titles, 1):
                            st.markdown(f"**{i}.** {title}")

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

# ============ ONGLET DESCRIPTION ============
with tab_description:
    video_description = st.text_area(
        "📝 Décrivez votre vidéo",
        placeholder="Ex: Une vidéo qui explique comment créer un stock de nourriture pour 3 mois en cas de crise, avec des conseils pratiques et un budget limité...",
        height=150,
        help="Décrivez brièvement le sujet et le contenu de votre vidéo"
    )

    num_titles_desc = st.slider(
        "📊 Nombre de titres",
        min_value=1,
        max_value=10,
        value=5,
        help="Choisissez combien de titres vous voulez générer",
        key="num_titles_desc"
    )

    if st.button("✨ Générer les titres", type="primary", use_container_width=True, key="btn_desc"):
        if not video_description or len(video_description.strip()) < 10:
            st.warning("⚠️ Veuillez entrer une description (minimum 10 caractères)")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("🤖 Génération des titres avec Claude...")
            progress_bar.progress(50)

            with st.spinner("Analyse par l'IA..."):
                result = generate_titles_from_description(video_description, anthropic_api_key, num_titles=num_titles_desc)

            progress_bar.progress(100)
            status_text.empty()

            titles = result.get("titles", [])
            raw_response = result.get("raw_response", "")
            has_custom_prompt = result.get("has_custom_prompt", False)

            if titles:
                st.success(f"✅ {len(titles)} titres générés avec succès!")
                st.markdown("---")

                if has_custom_prompt and raw_response:
                    st.subheader("🎯 Analyse complète des titres")
                    st.markdown(raw_response)
                else:
                    st.subheader("🎯 Propositions de titres")
                    for i, title in enumerate(titles, 1):
                        st.markdown(f"**{i}.** {title}")
            else:
                st.error("❌ Impossible de générer les titres. Vérifiez votre clé API.")

# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ Information")
    st.markdown("""
    ### Comment utiliser

    **Mode URL :**
    1. Collez le lien d'une vidéo YouTube
    2. Choisissez le nombre de titres
    3. Cliquez sur "Générer"

    **Mode Description :**
    1. Décrivez brièvement votre vidéo
    2. Choisissez le nombre de titres
    3. Cliquez sur "Générer"

    ### Fonctionnalités
    - ✅ Génération depuis URL ou description
    - ✅ Génération IA avec Claude Sonnet 4.5
    - ✅ Analyse Word Balance et scores
    - ✅ Titres optimisés SEO
    """)

    st.markdown("---")
    st.caption("🤖 Propulsé par Claude AI")
