from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import io

def axes_to_bytes(ax: plt.Axes) -> io.BytesIO:
    buf = io.BytesIO()
    ax.get_figure().savefig(buf)
    buf.seek(0)
    return buf

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

    return axes_to_bytes(ax)

def get_average_likes_by_hour(mongo: MongoClient):
    #db.getCollection('tweets').aggregate([{$group: {_id: {$hour: '$date_time'}, avgLikes: {$avg:  '$number_of_likes'}}}, {$sort: {_id: 1}}])
    cursor = mongo.get_database('insights').get_collection('tweets').aggregate(pipeline=[{"$group": {"_id": {"$hour": '$date_time'}, "avgLikes": {"$avg": '$number_of_likes'}}}, {"$sort": {"_id": 1}}])
    return list(cursor)

def get_average_likes_by_hour_plot(mongo: MongoClient) -> io.BytesIO:
    #db.getCollection('tweets').aggregate([{$group: {_id: {$hour: '$date_time'}, avgLikes: {$avg:  '$number_of_likes'}}}, {$sort: {_id: 1}}])
    items = get_average_likes_by_hour(mongo)
    y = [item['avgLikes'] for item in items]
    x = [item['_id'] for item in items]
    df = pd.DataFrame(y, index=x, columns=['avgLikes'])
    ax = df.plot(kind='bar', title='Average Likes by Hour', xlabel='Hour', ylabel='Average Likes')
    return axes_to_bytes(ax)

def get_count_by_length(mongo: MongoClient):
#     db.tweets.aggregate([
#   {
#     $group: {
#       _id: { $strLenCP: "$content" }, 
#       count: { $sum: 1 } 
#     }
#   },
#   {
#     $sort: { "_id": 1 }
#   }
# ])
    cursor = mongo.get_database('insights').get_collection('tweets') \
        .aggregate(pipeline=[{"$group": {"_id": {"$strLenCP": "$content"}, "count": {"$sum": 1}}}, 
                             {"$sort": {"_id": 1}}])
    return list(cursor)

def get_count_by_length_plot(mongo: MongoClient) -> io.BytesIO:
    items = get_count_by_length(mongo)
    #filter out tweets larger than 140 characters
    items = list(filter(lambda x: x['_id'] < 141, items))
    y = [item['count'] for item in items]
    x = [item['_id'] for item in items]
    df = pd.DataFrame(y, index=x, columns=['count'])
    ax = df.plot(kind='line', title='Count of tweets by Length', xlabel='Length', ylabel='Count')
    return axes_to_bytes(ax)

def get_avg_likes_by_length(mongo: MongoClient):
    # db.tweets.aggregate([
    #   {
    #     $group: {
    #       _id: { $strLenCP: "$content" }, 
    #       avgLikes: { $avg: "$number_of_likes" } 
    #     }
    #   },
    #   {
    #     $sort: { "_id": 1 }
    #   }
    # ])
    cursor = mongo.get_database('insights').get_collection('tweets') \
        .aggregate(pipeline=[{"$group": {"_id": {"$strLenCP": "$content"}, "avgLikes": {"$avg": "$number_of_likes"}}}, 
                             {"$sort": {"_id": 1}}])
    return list(cursor)

def get_avg_likes_by_length_plot(mongo: MongoClient):
    
    items = get_avg_likes_by_length(mongo)
    #filter out tweets larger than 140 characters
    items = list(filter(lambda x: x['_id'] < 141, items))
    y = [item['avgLikes'] for item in items]
    x = [item['_id'] for item in items]
    df = pd.DataFrame(y, index=x, columns=['avgLikes'])
    ax = df.plot(kind='line', title='avg likes by tweet Length', xlabel='Length', ylabel='avg likes')
    return axes_to_bytes(ax)

def get_avg_shares_by_length(mongo: MongoClient):
    # db.tweets.aggregate([
    #   {
    #     $group: {
    #       _id: { $strLenCP: "$content" }, 
    #       avgShares: { $avg: "$number_of_shares" } 
    #     }
    #   },
    #   {
    #     $sort: { "_id": 1 }
    #   }
    # ])
    cursor = mongo.get_database('insights').get_collection('tweets') \
        .aggregate(pipeline=[{"$group": {"_id": {"$strLenCP": "$content"}, "avgShares": {"$avg": "$number_of_shares"}}}, 
                             {"$sort": {"_id": 1}}])
    return list(cursor)

def get_avg_shares_by_length_plot(mongo: MongoClient):
    items = get_avg_shares_by_length(mongo)
    #filter out tweets larger than 140 characters
    items = list(filter(lambda x: x['_id'] < 141, items))
    y = [item['avgShares'] for item in items]
    x = [item['_id'] for item in items]
    df = pd.DataFrame(y, index=x, columns=['avgShares'])
    ax = df.plot(kind='line', title='avg shares by tweet Length', xlabel='Length', ylabel='avg shares')
    return axes_to_bytes(ax)