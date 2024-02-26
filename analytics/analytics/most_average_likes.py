from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import io

def get_most_average_likes(mongo: MongoClient):
    # db.getCollection('tweets').aggregate([{$group: {_id: '$author', avgLikes: {$avg: {$toInt: '$number_of_likes'}}}}, {$sort: {avgLikes: -1}}])
    cursor = mongo.get_database('insights').get_collection('tweets').aggregate(pipeline=[{"$group": {"_id": '$author', "avgLikes": {"$avg": 
        {"$toInt": '$number_of_likes'}}}}, {"$sort": {"avgLikes": -1}}])
    return list(cursor)

def get_most_average_likes_plot(mongo: MongoClient) -> io.BytesIO:
    # db.getCollection('tweets').aggregate([{$group: {_id: '$author', avgLikes: {$avg: {$toInt: '$number_of_likes'}}}}, {$sort: {avgLikes: -1}}])
    items = get_most_average_likes(mongo)
    y = [item['avgLikes'] for item in items]
    x = [item['_id'] for item in items]
    df = pd.DataFrame(y, index=x, columns=['avgLikes'])
    ax = df.plot(kind='bar', title='Average Likes by Author', xlabel='Author', ylabel='Average Likes')
    fig = ax.get_figure()
    
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return list(buf)