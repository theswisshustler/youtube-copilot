# 🔄 Guide d'Intégration n8n

Ce guide vous montre comment utiliser votre API dans n8n pour automatiser la génération de titres YouTube.

---

## 📋 Prérequis

1. ✅ Votre API est déployée (voir [DEPLOIEMENT_API.md](DEPLOIEMENT_API.md))
2. ✅ Vous avez l'URL de votre API (ex: `https://votre-api.onrender.com`)
3. ✅ Vous avez un compte n8n (Cloud ou Self-hosted)

---

## 🚀 Workflow n8n : Génération Automatique de Titres

### Scénario d'exemple

Vous voulez automatiquement générer des titres optimisés pour chaque nouvelle vidéo YouTube que vous publiez.

---

## 🔧 Configuration du Workflow n8n

### Étape 1 : Créer un nouveau workflow

1. Connectez-vous à n8n
2. Cliquez sur **"New Workflow"**
3. Nommez-le : "YouTube Title Generator"

---

### Étape 2 : Ajouter le trigger (déclencheur)

**Option A : Webhook (déclenché manuellement ou par un autre service)**

1. Ajoutez un node **"Webhook"**
2. Configurez :
   - **HTTP Method** : `POST`
   - **Path** : `youtube-titles`
   - **Response** : `Immediately`

**Option B : Schedule (automatique à intervalles réguliers)**

1. Ajoutez un node **"Schedule Trigger"**
2. Configurez la fréquence (ex: tous les jours à 9h)

**Option C : Google Sheets (quand vous ajoutez une ligne)**

1. Ajoutez un node **"Google Sheets Trigger"**
2. Connectez votre compte Google
3. Sélectionnez votre feuille avec les URLs YouTube

---

### Étape 3 : Ajouter le node HTTP Request

1. Cliquez sur **"+"** pour ajouter un node
2. Cherchez et sélectionnez **"HTTP Request"**
3. Configurez comme suit :

**Configuration :**
```
Authentication: None
Request Method: POST
URL: https://votre-api.onrender.com/generate-titles

Headers:
- Name: Content-Type
- Value: application/json

Body Content Type: JSON
Specify Body: Using JSON

JSON Body:
{
  "youtube_url": "{{ $json.youtube_url }}",
  "num_titles": 5
}
```

**Si vous utilisez un webhook, le JSON sera :**
```json
{
  "youtube_url": "{{ $json.body.youtube_url }}",
  "num_titles": 5
}
```

---

### Étape 4 : Traiter la réponse

La réponse de l'API ressemble à :
```json
{
  "success": true,
  "titles": [
    "Titre 1",
    "Titre 2",
    "Titre 3",
    "Titre 4",
    "Titre 5"
  ],
  "transcript_length": 15430,
  "error": null
}
```

---

### Étape 5 : Que faire avec les titres ?

**Option A : Envoyer par email**

1. Ajoutez un node **"Gmail"** ou **"Send Email"**
2. Configurez :
   ```
   To: votre@email.com
   Subject: Nouveaux titres pour votre vidéo
   Body:
   Voici vos 5 titres générés :

   1. {{ $json.titles[0] }}
   2. {{ $json.titles[1] }}
   3. {{ $json.titles[2] }}
   4. {{ $json.titles[3] }}
   5. {{ $json.titles[4] }}
   ```

**Option B : Sauvegarder dans Google Sheets**

1. Ajoutez un node **"Google Sheets"**
2. Configurez :
   - **Operation** : Append
   - **Sheet** : Votre feuille
   - Mappez les titres dans les colonnes

**Option C : Envoyer sur Slack/Discord**

1. Ajoutez un node **"Slack"** ou **"Discord"**
2. Configurez le message avec les titres

**Option D : Enregistrer dans une base de données**

1. Ajoutez un node **"Airtable"**, **"Notion"**, ou **"PostgreSQL"**
2. Sauvegardez les titres

---

## 🎬 Exemples de Workflows Complets

### Workflow 1 : Webhook → API → Email

```
[Webhook]
  ↓ (Reçoit youtube_url)
[HTTP Request: Génération de titres]
  ↓ (Reçoit les 5 titres)
[Gmail: Envoi des titres par email]
```

**Utilisation :**
```bash
curl -X POST "https://votre-n8n.app/webhook/youtube-titles" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

### Workflow 2 : Google Sheets → API → Update Sheets

```
[Google Sheets Trigger: Nouvelle ligne ajoutée]
  ↓ (Contient youtube_url dans colonne A)
[HTTP Request: Génération de titres]
  ↓ (Reçoit les 5 titres)
[Google Sheets: Update la même ligne]
  ↓ (Ajoute les titres dans colonnes B-F)
```

**Utilisation :**
1. Ajoutez une URL YouTube dans la colonne A
2. Les titres apparaissent automatiquement dans les colonnes B-F

---

### Workflow 3 : Schedule → RSS Feed → API → Slack

```
[Schedule: Tous les jours à 9h]
  ↓
[RSS Feed: Récupère les dernières vidéos]
  ↓ (Pour chaque vidéo)
[HTTP Request: Génération de titres]
  ↓ (Reçoit les 5 titres)
[Slack: Poste dans #youtube-titles]
```

---

## 🔍 Exemple de Configuration Complète

### Node HTTP Request - Configuration Détaillée

```yaml
Node: HTTP Request
Name: Generate YouTube Titles

Authentication: None
Request Method: POST
URL: https://youtube-title-generator-api.onrender.com/generate-titles

Options:
  Response Format: JSON
  Timeout: 30000 (30 secondes)

Headers:
  - Name: Content-Type
    Value: application/json

Body:
  {
    "youtube_url": "{{ $json.youtube_url }}",
    "num_titles": 5
  }
```

### Node Email - Configuration Détaillée

```yaml
Node: Gmail
Name: Send Titles Email

To: {{ $json.user_email }}
Subject: 🎬 Titres générés pour votre vidéo YouTube

Email Type: HTML

Body:
<h2>Vos titres YouTube sont prêts !</h2>

<p>Voici 5 propositions de titres optimisés :</p>

<ol>
  <li><strong>{{ $('HTTP Request').item.json.titles[0] }}</strong></li>
  <li><strong>{{ $('HTTP Request').item.json.titles[1] }}</strong></li>
  <li><strong>{{ $('HTTP Request').item.json.titles[2] }}</strong></li>
  <li><strong>{{ $('HTTP Request').item.json.titles[3] }}</strong></li>
  <li><strong>{{ $('HTTP Request').item.json.titles[4] }}</strong></li>
</ol>

<p><small>Transcription : {{ $('HTTP Request').item.json.transcript_length }} caractères</small></p>
```

---

## 🔧 Gestion des Erreurs

### Ajouter une condition pour vérifier le succès

1. Après le node HTTP Request, ajoutez un node **"IF"**
2. Configurez :
   ```
   Value 1: {{ $json.success }}
   Operation: Equal
   Value 2: true
   ```

3. **Si true** → Continuez le workflow normal
4. **Si false** → Envoyez une notification d'erreur

### Node d'erreur pour Slack

```yaml
Node: Slack
Channel: #errors

Message:
❌ Erreur lors de la génération de titres

Vidéo: {{ $json.youtube_url }}
Erreur: {{ $('HTTP Request').item.json.error }}
```

---

## 💡 Astuces et Bonnes Pratiques

### 1. Utiliser des variables pour l'URL de l'API

Dans les paramètres du workflow, créez une variable :
- **Name** : `API_URL`
- **Value** : `https://votre-api.onrender.com`

Utilisez-la dans le node HTTP Request : `{{ $workflow.settings.API_URL }}/generate-titles`

### 2. Ajouter un délai entre les requêtes

Si vous traitez plusieurs vidéos, ajoutez un node **"Wait"** entre chaque requête pour éviter le rate limiting.

### 3. Sauvegarder les résultats

Toujours sauvegarder les titres générés dans une base de données ou un fichier pour ne pas les perdre.

### 4. Tester avec le mode manuel

Activez **"Execute Workflow"** manuellement pour tester avant d'activer le workflow automatique.

---

## 📊 Templates de Workflows Prêts à l'Emploi

### Template JSON pour n8n

Copiez ce JSON et importez-le dans n8n (**Import from URL or File**) :

```json
{
  "name": "YouTube Title Generator",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "youtube-titles",
        "responseMode": "responseNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://votre-api.onrender.com/generate-titles",
        "jsonParameters": true,
        "options": {},
        "bodyParametersJson": "={\n  \"youtube_url\": \"{{ $json.body.youtube_url }}\",\n  \"num_titles\": 5\n}"
      },
      "name": "Generate Titles",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "Generate Titles", "type": "main", "index": 0}]]
    }
  }
}
```

**Remplacez** : `https://votre-api.onrender.com` par votre vraie URL d'API

---

## 🎯 Cas d'Usage Avancés

### 1. A/B Testing de titres

Générez plusieurs sets de titres et testez lesquels performent le mieux.

### 2. Génération multilingue

Appelez l'API plusieurs fois pour générer des titres en français, anglais, espagnol, etc.

### 3. Pipeline de publication

```
Nouvelle vidéo → Génération titres → Choix automatique → Mise à jour YouTube → Notification
```

---

## 🆘 Dépannage

### "Connection timeout"
→ L'API Render dort après 15min d'inactivité. La première requête prend 30s.

### "Invalid JSON"
→ Vérifiez que le Body est bien en format JSON et pas en form-data

### "API Key not configured"
→ Vérifiez les variables d'environnement sur Render/Railway

### Les titres sont vides
→ La vidéo n'a probablement pas de transcription disponible

---

## 🎉 Vous êtes prêt !

Votre workflow n8n est maintenant configuré pour automatiser la génération de titres YouTube !

**Prochaines étapes :**
1. ✅ Testez le workflow manuellement
2. ✅ Activez le workflow
3. ✅ Surveillez les logs pour détecter les erreurs
4. ✅ Optimisez selon vos besoins

---

**Besoin d'aide ?** Consultez la documentation n8n : https://docs.n8n.io
