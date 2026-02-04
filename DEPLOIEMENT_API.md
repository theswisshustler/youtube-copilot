# 🚀 Guide de Déploiement de l'API REST

Ce guide vous explique comment déployer votre API sur un service cloud gratuit.

---

## 🎯 Option 1 : Déployer sur Render.com (Recommandé - 100% Gratuit)

### Étape 1 : Créer un compte Render

1. Allez sur https://render.com
2. Cliquez sur "Get Started" (Commencer)
3. Inscrivez-vous avec GitHub (le plus simple)
4. Autorisez Render à accéder à votre compte GitHub

### Étape 2 : Créer un nouveau Web Service

1. Une fois connecté, cliquez sur **"New +"** → **"Web Service"**

2. Connectez votre dépôt GitHub :
   - Sélectionnez `theswisshustler/youtube-copilot`
   - Cliquez sur "Connect"

3. Configurez le service :
   - **Name** : `youtube-title-generator-api` (ou votre nom)
   - **Region** : Europe (Paris/Frankfurt) ou closest to you
   - **Branch** : `main`
   - **Root Directory** : laissez vide
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements-api.txt`
   - **Start Command** : `uvicorn api:app --host 0.0.0.0 --port $PORT`

4. Plan :
   - Sélectionnez **"Free"** (Gratuit)
   - Note: L'app peut s'endormir après 15 min d'inactivité (réveil en 30s)

5. Variables d'environnement :
   - Cliquez sur **"Advanced"**
   - Ajoutez une variable d'environnement :
     - **Key** : `ANTHROPIC_API_KEY`
     - **Value** : `votre_clé_anthropic_ici` (récupérez-la depuis votre fichier .env)

6. Cliquez sur **"Create Web Service"**

### Étape 3 : Attendre le déploiement

⏳ Le déploiement prend 2-5 minutes
- Vous verrez les logs en temps réel
- Attendez le message "Your service is live 🎉"

### Étape 4 : Tester votre API

Votre API sera accessible à : `https://youtube-title-generator-api.onrender.com`

Testez-la :
```bash
# Vérifier la santé
https://youtube-title-generator-api.onrender.com/health

# Documentation interactive
https://youtube-title-generator-api.onrender.com/docs
```

---

## 🎯 Option 2 : Déployer sur Railway.app

### Étape 1 : Créer un compte Railway

1. Allez sur https://railway.app
2. Cliquez sur "Start a New Project"
3. Connectez-vous avec GitHub

### Étape 2 : Déployer depuis GitHub

1. Cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez `theswisshustler/youtube-copilot`

### Étape 3 : Configurer le projet

1. Une fois le projet créé, allez dans **"Settings"**

2. Ajoutez les variables d'environnement :
   - Cliquez sur **"Variables"**
   - Ajoutez : `ANTHROPIC_API_KEY` = `votre_clé_ici`

3. Configurez le démarrage :
   - Dans **"Settings"** → **"Deploy"**
   - **Build Command** : `pip install -r requirements-api.txt`
   - **Start Command** : `uvicorn api:app --host 0.0.0.0 --port $PORT`

4. Railway déploiera automatiquement

### Étape 4 : Obtenir l'URL publique

1. Dans votre projet, allez dans **"Settings"** → **"Networking"**
2. Cliquez sur **"Generate Domain"**
3. Votre API sera accessible à : `https://votre-projet.up.railway.app`

---

## 🧪 Tester votre API

### Via le navigateur

Allez sur : `https://votre-api-url.com/docs`

Vous verrez une documentation interactive (Swagger UI) où vous pouvez :
- ✅ Voir tous les endpoints
- ✅ Tester directement dans le navigateur
- ✅ Voir les exemples de requêtes/réponses

### Via curl (ligne de commande)

```bash
# Vérifier la santé de l'API
curl https://votre-api-url.com/health

# Générer des titres
curl -X POST "https://votre-api-url.com/generate-titles" \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "num_titles": 5
  }'
```

### Via n8n (voir GUIDE_N8N.md)

Utilisez le node "HTTP Request" dans n8n pour appeler votre API.

---

## 📊 Comparaison des plateformes

| Critère | Render.com | Railway.app |
|---------|-----------|-------------|
| **Prix gratuit** | ✅ Oui | ✅ Oui (5$/mois de crédit) |
| **Déploiement** | Très simple | Très simple |
| **Performance** | Excellente | Excellente |
| **Limitations free** | Dort après 15min inactivité | 500h/mois d'exécution |
| **Déploiement auto** | ✅ Oui | ✅ Oui |

**Recommandation** : Render.com pour un usage occasionnel, Railway pour un usage intensif.

---

## 🔄 Mises à jour automatiques

Les deux plateformes détectent automatiquement les changements sur GitHub :
- Chaque `git push` déclenche un nouveau déploiement
- L'API est mise à jour automatiquement
- Pas besoin de redéployer manuellement

---

## 🔐 Sécurité

⚠️ **Important** : Ne committez JAMAIS votre clé API dans le code !
- ✅ Toujours utiliser les variables d'environnement
- ✅ Le fichier `.env` est déjà dans `.gitignore`
- ✅ Configurez la clé dans les paramètres de la plateforme

---

## 🆘 Dépannage

### "Module not found"
→ Vérifiez que `requirements-api.txt` est bien dans le repo

### "Port already in use"
→ Normal en développement local, ignorez sur les plateformes cloud

### "API Key not found"
→ Vérifiez que `ANTHROPIC_API_KEY` est configuré dans les variables d'environnement

### Logs en production
- **Render** : Onglet "Logs" dans votre service
- **Railway** : Onglet "Deployments" → cliquez sur le déploiement

---

## 🎉 Prochaines étapes

Une fois votre API déployée :
1. ✅ Notez l'URL de votre API
2. ✅ Testez avec `/docs`
3. ✅ Consultez **GUIDE_N8N.md** pour l'intégration dans n8n
4. ✅ Commencez à automatiser vos titres YouTube !

---

**Besoin d'aide ?** Vérifiez les logs de déploiement pour identifier les erreurs.
