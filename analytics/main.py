from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pymongo import MongoClient
from services.mongo import connect_to_mongo
import analytics as analytics
import uvicorn
import dotenv
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


@app.get("/analytics/_health")
async def health():
    return 'ok'


@app.get("/analytics/api/most_average_likes")
def most_average_likes():
    return analytics.get_most_average_likes(connection)

@app.get("/analytics/api/most_average_likes/image")
def most_average_likes_plot():
    buf= analytics.get_most_average_likes_plot(connection)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/analytics/api/avg_likes_by_hour")
def avg_likes_by_hour():
    return analytics.get_average_likes_by_hour(connection)

@app.get("/analytics/api/avg_likes_by_hour/image")
def avg_likes_by_hour_plot():
    buf= analytics.get_average_likes_by_hour_plot(connection)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/analytics/api/count_by_length")
def count_by_length():
    return analytics.get_count_by_length(connection)

@app.get("/analytics/api/count_by_length/image")
def count_by_length_plot():
    buf= analytics.get_count_by_length_plot(connection)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/analytics/api/avg_likes_by_length")
def avg_likes_by_len():
    return analytics.get_avg_likes_by_length(connection)

@app.get("/analytics/api/avg_likes_by_length/image")
def avg_likes_by_len_plot():
    buf= analytics.get_avg_likes_by_length_plot(connection)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/analytics/api/avg_shares_by_length/image")
def avg_shares_by_len_plot():
    buf= analytics.get_avg_shares_by_length_plot(connection)
    return StreamingResponse(buf, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)