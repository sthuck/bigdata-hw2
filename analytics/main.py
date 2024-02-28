from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pymongo import MongoClient
from services.mongo import connect_to_mongo
from analytics.most_average_likes import get_most_average_likes, get_most_average_likes_plot
import uvicorn
import dotenv

dotenv.load_dotenv()
connection: MongoClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection
    connection = connect_to_mongo()
    yield
    connection.close()

app = FastAPI(lifespan=lifespan)


@app.get("/analytics/_health")
async def health():
    return 'ok'


@app.get("/analytics/api/most_average_likes")
def most_average_likes():
    return get_most_average_likes(connection)

@app.get("/analytics/api/most_average_likes/image")
def most_average_likes_plot():
    buf= get_most_average_likes_plot(connection)
    return StreamingResponse(buf, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)