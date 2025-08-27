## FastAPIMongoAPI

Dynamic FastAPI REST API with MongoDB Atlas. Entity/collection is provided at request time. JSON bodies are saved as-is (no Pydantic models). ObjectIds are serialized to strings in responses.

### Endpoints
- `GET /{entity}`: Fetch all documents
- `GET /{entity}/{item_id}`: Fetch document by ObjectId
- `POST /{entity}`: Save a new JSON object as-is
- `PUT /{entity}/{item_id}`: Update fields on an existing document

### Prerequisites
- Python 3.9+
- MongoDB Atlas connection string

### Setup
```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1  # PowerShell on Windows
pip install -r requirements.txt

# Configure environment
$env:MONGODB_URI = "YOUR_ATLAS_CONNECTION_STRING"
$env:MONGODB_DB = "YOUR_DATABASE_NAME"

# Run locally
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Example
```bash
curl http://localhost:8000/users
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"name":"Ada"}'
```

### GitHub
Initialize and commit:
```powershell
git init
git add -A
git commit -m "feat: initial FastAPI + MongoDB API scaffold"
```

Add remote and push (replace with your repo URL):
```powershell
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main
```

### Deploy on Render
1. Push the repo to GitHub
2. In Render, create a new Web Service from your repo
3. Environment: `Python 3`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables: `MONGODB_URI`, `MONGODB_DB`


