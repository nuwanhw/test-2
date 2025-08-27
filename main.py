from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId
import os


app = FastAPI(title="FastAPIMongoAPI", description="Dynamic entity FastAPI + MongoDB Atlas API")


def get_db():
    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONGODB_DB")
    if not mongodb_uri or not database_name:
        raise RuntimeError("Environment variables MONGODB_URI and MONGODB_DB must be set")
    client = MongoClient(mongodb_uri)
    return client[database_name]


def serialize_document(document: dict) -> dict:
    if not document:
        return document
    doc = {**document}
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc


@app.get("/")
def health() -> dict:
    return {"status": "ok"}


@app.get("/{entity}")
def get_all(entity: str):
    db = get_db()
    collection = db[entity]
    documents = list(collection.find())
    serialized = [serialize_document(d) for d in documents]
    return JSONResponse(content=serialized)


@app.get("/{entity}/{item_id}")
def get_by_id(entity: str, item_id: str = Path(..., description="MongoDB ObjectId")):
    db = get_db()
    collection = db[entity]
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    document = collection.find_one({"_id": oid})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return JSONResponse(content=serialize_document(document))


@app.post("/{entity}")
async def save_new(entity: str, body: dict):
    db = get_db()
    collection = db[entity]
    result = collection.insert_one(body)
    created = collection.find_one({"_id": result.inserted_id})
    return JSONResponse(content=serialize_document(created))


@app.put("/{entity}/{item_id}")
async def update(entity: str, item_id: str, body: dict):
    db = get_db()
    collection = db[entity]
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    update_result = collection.update_one({"_id": oid}, {"$set": body})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    updated = collection.find_one({"_id": oid})
    return JSONResponse(content=serialize_document(updated))


# For local dev: uvicorn main:app --reload

