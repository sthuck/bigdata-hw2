from pymongo import MongoClient
import csv
from datetime import datetime

def ingest(mongo: MongoClient):
    db = mongo['insights']
    collection = db['tweets']
    with open("data/tweets.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        # Insert each row as a dictionary
        for chunk in lazy_chunk(reader, 400):
            collection.insert_many(chunk)

def is_ingested(mongo: MongoClient):
    db = mongo['insights']
    collection = db['tweets']
    return collection.count_documents({}) > 0

def clear_dataset(mongo: MongoClient):
    db = mongo['insights']
    collection = db['tweets']
    collection.delete_many({})


def transform_row(row):
    row['number_of_likes'] = int(row['number_of_likes'])
    row['number_of_shares'] = int(row['number_of_shares'])
    row['date_time'] = parse_date(row['date_time'])
    return row

def parse_date(date_str) -> datetime:
    date_time_list = date_str.split(" ")
    date_str = date_time_list[0]
    time_str = date_time_list[1]

    # Define format specifiers for date and time
    date_format = "%d/%m/%Y"
    time_format = "%H:%M"

    # Parse the date and time components separately
    date_obj = datetime.strptime(date_str, date_format)
    time_obj = datetime.strptime(time_str, time_format)

    # Combine the date and time objects into a single datetime object
    datetime_obj = datetime.combine(date_obj, time_obj.time())
    return datetime_obj
    
def lazy_chunk(iterator, chunk_size):
    """Lazily splits an iterator into chunks of a given size.

    Args:
        iterator: An iterator to split.
        chunk_size: The size of each chunk.

    Yields:
        Chunks of the iterator as lists.
    """
    chunk = []
    for row in iterator:
        chunk.append(transform_row(row))
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
