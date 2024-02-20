
import os
import httpx

# this code doesn't work due to twitter api restrictions

def get_access_token() -> str:
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    if client_id is None or client_secret is None:
        print('Please set CLIENT_ID and CLIENT_SECRET in .env file')
        raise SystemExit(1)
    print(f'client_id: {client_id}')
    print(f'client_secret: {client_secret}')
    
    response = httpx.post('https://api.twitter.com/oauth2/token',
                          data={'grant_type': 'client_credentials'}, auth=(client_id, client_secret))
    return response.json().get('access_token')

def search_tweets(query: str, access_token: str) -> dict:
    response = httpx.get('https://api.twitter.com/1.1/search/tweets.json', 
                         headers={'Authorization': f'Bearer {access_token}'}, params={'q': query})
    return response.json()