import dotenv
from dataset import ingest

from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import MongoClient
from services.mongo import connect_to_mongo
import uvicorn

dotenv.load_dotenv()
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

@app.post("/ingestor/api/ingest_dataset")
def ingest_dataset():
    return ingest(connection)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)