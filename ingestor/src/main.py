import dotenv
from dataset import ingest, is_ingested, clear_dataset

from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import MongoClient
from services.mongo import connect_to_mongo
import uvicorn
import os
dotenv.load_dotenv()

port = int(os.environ.get('PORT', 8000))
connection: MongoClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection
    connection = connect_to_mongo()
    yield
    connection.close()

app = FastAPI(lifespan=lifespan)


@app.get("/ingestor/_health")
def health():
    return 'ok'

@app.post("/ingestor/api/dataset/ingest")
def ingest_dataset():
    return ingest(connection)

@app.get("/ingestor/api/dataset")
def check():
    return is_ingested(connection)

@app.delete("/ingestor/api/dataset")
def clear():
    return clear_dataset(connection)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)