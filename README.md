# CASCADE API

API FastAPI permettant à STELLA MASTER d'exécuter des commandes de manière autonome.

## 🎯 Objectif

Permettre à STELLA MASTER (bot Telegram) d'exécuter des tâches techniques sans intervention manuelle:

- Exécuter des commandes système
- Créer et éditer des fichiers
- Faire des commits Git
- Gérer le projet de manière autonome

## 🔧 Endpoints

### 1. Execute Command

```bash
POST /api/execute_command
Authorization: Bearer <API_KEY>

{
  "command": "npm install jest",
  "cwd": "/path/to/project",
  "timeout": 300
}
```

### 2. Create File

```bash
POST /api/create_file
Authorization: Bearer <API_KEY>

{
  "path": "/path/to/file.js",
  "content": "console.log('hello');",
  "overwrite": false
}
```

### 3. Edit File

```bash
POST /api/edit_file
Authorization: Bearer <API_KEY>

{
  "path": "/path/to/file.js",
  "old_string": "hello",
  "new_string": "world"
}
```

### 4. Read File

```bash
POST /api/read_file
Authorization: Bearer <API_KEY>

{
  "path": "/path/to/file.js"
}
```

### 5. Git Commit

```bash
POST /api/git_commit
Authorization: Bearer <API_KEY>

{
  "message": "Add tests",
  "files": ["test.js"],
  "push": true
}
```

### 6. Git Status

```bash
GET /api/git_status
Authorization: Bearer <API_KEY>
```

## 🔐 Sécurité

- **API Key**: Requise dans header `Authorization: Bearer <key>`
- **Path validation**: Tous les chemins doivent être dans PROJECT_ROOT
- **Timeout**: Commandes limitées à 300s par défaut
- **Rate limiting**: À implémenter en production

## 🚀 Déploiement

### Local

```bash
cd cascade-api
source venv/bin/activate
python main.py
```

### Railway

1. Connecter repo GitHub: `bmapbenoit-ctrl/cascade-api`
2. Configurer variables:
   - `CASCADE_API_KEY`
   - `PROJECT_ROOT=/app`
   - `ALLOWED_IPS=*`
3. Déployer

## 📊 Stack

- **FastAPI**: Framework web async
- **Uvicorn**: Serveur ASGI
- **GitPython**: Opérations Git
- **Pydantic**: Validation données

## 🔗 Intégration STELLA MASTER

Ajouter function calling dans le bot:

```javascript
{
  name: 'execute_cascade_command',
  description: 'Exécuter une commande via CASCADE API',
  parameters: {
    command: { type: 'string' },
    cwd: { type: 'string' }
  }
}
```

## 📝 Variables d'environnement

```env
CASCADE_API_KEY=cascade_master_2026_secure_key_stella
PROJECT_ROOT=/Users/planetebeauty/Documents/copilote-planetebeauty
ALLOWED_IPS=*
PORT=8000
```

## ✅ Tests

```bash
# Health check
curl http://localhost:8000/health

# Execute command
curl -X POST http://localhost:8000/api/execute_command \
  -H "Authorization: Bearer cascade_master_2026_secure_key_stella" \
  -H "Content-Type: application/json" \
  -d '{"command": "echo test"}'
```

## 📄 License

MIT

## 👤 Author

CASCADE - Développé pour STELLA MASTER
