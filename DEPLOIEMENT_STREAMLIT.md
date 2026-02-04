# 🚀 Guide de Déploiement sur Streamlit Cloud

## 📋 Étape 1 : Créer un compte Streamlit Cloud

1. Allez sur https://streamlit.io/cloud
2. Cliquez sur "Sign up" (s'inscrire)
3. **Choisissez "Continue with GitHub"** (c'est le plus simple)
4. Autorisez Streamlit à accéder à votre compte GitHub

## 🔗 Étape 2 : Déployer votre application

1. Une fois connecté, cliquez sur **"New app"** (Nouvelle application)

2. Remplissez les informations :
   - **Repository** : `theswisshustler/youtube-copilot`
   - **Branch** : `main`
   - **Main file path** : `app_web.py`
   - **App URL** : choisissez un nom personnalisé (ex: `youtube-title-gen`)

3. Cliquez sur **"Deploy!"**

⏳ L'application va commencer à se déployer (cela prend 2-3 minutes)

## 🔐 Étape 3 : Configurer les secrets (IMPORTANT!)

Pendant le déploiement, l'app va échouer car les clés API ne sont pas configurées. C'est normal !

1. Dans la page de votre app sur Streamlit Cloud, cliquez sur **"Settings"** (⚙️ en haut à droite)

2. Allez dans l'onglet **"Secrets"**

3. Copiez-collez ce format TOML avec VOS vraies clés :

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."
YOUTUBE_TRANSCRIPT_API_TOKEN = "votre_token_youtube_transcript"
```

4. Cliquez sur **"Save"** (Sauvegarder)

5. L'application va automatiquement redémarrer avec les secrets configurés

## ✅ Étape 4 : Tester votre application

1. Attendez que l'application redémarre (environ 30 secondes)
2. Votre app sera accessible à l'URL : `https://votre-nom-app.streamlit.app`
3. Testez avec une URL YouTube !

## 🌐 Étape 5 : Partager votre application

Vous pouvez maintenant :
- ✅ Partager l'URL avec votre équipe
- ✅ Utiliser l'app depuis n'importe quel appareil (PC, mobile, tablette)
- ✅ Épingler l'URL dans vos favoris

## 📱 Accès mobile

L'application fonctionne parfaitement sur mobile :
- Ajoutez l'URL à l'écran d'accueil de votre téléphone
- Elle fonctionnera comme une vraie app !

## 🔧 Mises à jour futures

Chaque fois que vous faites `git push` sur GitHub :
- Streamlit Cloud détecte automatiquement les changements
- L'application se redéploie automatiquement
- Vos utilisateurs voient les mises à jour immédiatement

## ⚠️ Limites de la version gratuite

- ✅ Illimité en nombre d'utilisateurs
- ✅ Toujours en ligne (24/7)
- ⚠️ L'app peut s'endormir après inactivité (réveil en 2-3 secondes)
- ⚠️ Ressources limitées (suffisant pour cet usage)

## 🆘 Dépannage

### "Module not found"
→ Vérifiez que toutes les dépendances sont dans `requirements.txt`

### "Secrets not found"
→ Vérifiez que vous avez bien configuré les secrets dans Settings

### L'app ne démarre pas
→ Consultez les logs dans l'interface Streamlit Cloud

## 🎉 C'est terminé !

Votre application est maintenant accessible partout dans le monde !
