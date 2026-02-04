# 🎬 Guide d'Utilisation - Générateur de Titres YouTube

## 🚀 Comment utiliser votre employé spécialisé partout et tout le temps

Vous avez 4 façons d'utiliser votre générateur de titres YouTube :

---

## ✅ Option 1 : Double-clic rapide (Le plus simple)

**Pour qui ?** Débutants, utilisation ponctuelle

**Comment ?**
1. Double-cliquez sur `lancer.bat`
2. Entrez l'URL de votre vidéo YouTube
3. Récupérez vos titres !

**Avantages :**
- ✅ Aucune installation supplémentaire
- ✅ Fonctionne immédiatement
- ✅ Interface en ligne de commande simple

---

## 🌟 Option 2 : Interface Web (Recommandé ⭐)

**Pour qui ?** Tout le monde, utilisation régulière

**Installation (une seule fois) :**
```bash
cd c:\Users\louis\youtube-title-generator
.\venv\Scripts\activate
pip install streamlit
```

**Utilisation :**
1. Double-cliquez sur `lancer_web.bat`
2. Votre navigateur s'ouvre automatiquement
3. Collez l'URL et générez vos titres dans une belle interface

**Avantages :**
- ✅ Interface graphique moderne
- ✅ Facile à utiliser
- ✅ Copier les titres en un clic
- ✅ Statistiques en temps réel
- ✅ Accessible depuis n'importe quel navigateur

**Raccourci pratique :**
- Créez un raccourci de `lancer_web.bat` sur votre bureau
- Épinglez-le à la barre des tâches Windows

---

## ⚡ Option 3 : Commande globale (Pour power users)

**Pour qui ?** Utilisateurs avancés qui travaillent dans le terminal

**Installation (une seule fois) :**
1. Double-cliquez sur `installer_commande.bat`
2. Fermez et rouvrez votre terminal
3. Tapez `youtube-titles` depuis n'importe où !

**Utilisation :**
```bash
# Depuis n'importe quel dossier
youtube-titles
```

**Avantages :**
- ✅ Accessible depuis n'importe où
- ✅ Rapide à lancer
- ✅ Parfait pour intégration dans scripts

---

## 🌐 Option 4 : Application Web hébergée (Accessible partout)

**Pour qui ?** Accès depuis n'importe quel appareil (PC, téléphone, tablette)

**Déploiement sur Streamlit Cloud (gratuit) :**

1. Créez un compte sur https://streamlit.io/cloud
2. Connectez votre compte GitHub
3. Poussez votre code sur GitHub :
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <votre-repo-github>
   git push -u origin main
   ```
4. Déployez sur Streamlit Cloud
5. Configurez vos clés API dans les secrets

**Avantages :**
- ✅ Accessible depuis n'importe où (PC, mobile, tablette)
- ✅ Pas d'installation locale nécessaire
- ✅ Partageable avec votre équipe
- ✅ Gratuit (avec limites Streamlit Cloud)

---

## 💡 Mes Recommandations

### Usage personnel quotidien
→ **Option 2 : Interface Web locale** avec raccourci sur le bureau

### Usage dans vos scripts/workflows
→ **Option 3 : Commande globale** `youtube-titles`

### Partage avec votre équipe
→ **Option 4 : Déploiement web** sur Streamlit Cloud

### Rapidité maximale
→ **Option 1 : Script batch** `lancer.bat`

---

## 🔧 Créer un raccourci bureau

**Pour l'interface web :**
1. Clic droit sur `lancer_web.bat`
2. "Envoyer vers" → "Bureau (créer un raccourci)"
3. Renommez en "📺 Générateur Titres YouTube"
4. Clic droit → Propriétés → Changer l'icône (optionnel)

**Pour accès encore plus rapide :**
- Épinglez le raccourci à la barre des tâches
- Assignez un raccourci clavier (Propriétés → Touche de raccourci)

---

## 🎯 Automatisation avancée

### Intégration dans un workflow
Créez votre propre script Python :

```python
from youtube_api import get_transcript_from_url
from title_generator import generate_titles
import os

# Récupérer automatiquement depuis une liste
videos = [
    "https://www.youtube.com/watch?v=...",
    "https://www.youtube.com/watch?v=..."
]

for video_url in videos:
    transcript = get_transcript_from_url(video_url)
    if transcript:
        titles = generate_titles(
            transcript,
            os.getenv("ANTHROPIC_API_KEY"),
            num_titles=5
        )
        print(f"\nTitres pour {video_url}:")
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")
```

---

## 📱 Accès mobile

Pour utiliser sur votre téléphone/tablette :

1. **Option simple :** Déployez l'interface web (Option 4)
2. **Option avancée :** Utilisez Termux sur Android + SSH vers votre PC

---

## 🔐 Sécurité

- ⚠️ Ne partagez JAMAIS votre fichier `.env`
- ⚠️ Ne committez JAMAIS vos clés API sur GitHub
- ✅ Utilisez les "Secrets" de Streamlit Cloud pour le déploiement

---

## ❓ Dépannage

**"Commande introuvable"**
→ Vérifiez que vous avez fermé/rouvert le terminal après l'installation

**"Erreur d'encodage"**
→ Vérifiée automatiquement par le code, normalement résolu

**"Clé API invalide"**
→ Vérifiez votre fichier `.env`

**"Pas de transcription trouvée"**
→ La vidéo doit avoir des sous-titres (automatiques ou manuels)

---

## 🆘 Support

Pour toute question :
1. Vérifiez ce guide d'abord
2. Consultez le README.md
3. Testez avec `lancer.bat` pour des logs détaillés

---

**Bon courage avec vos vidéos YouTube ! 🚀**
