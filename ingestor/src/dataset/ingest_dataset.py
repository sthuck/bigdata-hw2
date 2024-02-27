from pymongo import MongoClient
import csv

def ingest(mongo: MongoClient):
    db = mongo['insights']
    collection = db['tweets']
    with open("data/tweets.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        # Insert each row as a dictionary
        for chunk in lazy_chunk(reader, 50):
            collection.insert_many(chunk)


def lazy_chunk(iterator, chunk_size):
    """Lazily splits an iterator into chunks of a given size.

    Args:
        iterator: An iterator to split.
        chunk_size: The size of each chunk.

    Yields:
        Chunks of the iterator as lists.
    """
    chunk = []
    for item in iterator:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
