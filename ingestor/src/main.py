import httpx
import dotenv
import os
from dataset import connect_to_mongo, ingest

def main():
    dotenv.load_dotenv()
    mongo = connect_to_mongo()
    ingest(mongo)

    
# 
if __name__ == '__main__':
    main()