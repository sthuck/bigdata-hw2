# Final Project

### deployment 
simply run `kubectl apply -R -f k8s` . Files are named in a way that kubectl will apply them in the correct order

This project has 3 services:

- Ingestor, responsible for ingesting static data into mongo
- scraper, which allows to you to ingest data from twitter API. But it's very limited, and you get 429 error (too many requests) quite often.
- Analytics, which queries mongo, and uses pandas + matplotlib to output graphs
- ui, which provides a basic UI to run the ingestion and see the graphs


Ingestor and analtics are web api using FastAPI and python. They are package managed, by `poetry`, so poetry is needed to run services localy. Each project has a `local-dev.sh` file allowing local work with k8s cluster, using a tool called `telepresence`.

ui is a static website (html + js) served by nginx.

Images are built using github actions to github container registry.

### Scraper

scraper is written in node.js, and requires you to supply an API_KEY env var.
please see here on how to get API_KEY - https://github.com/Rishikant181/Rettiwt-API?tab=readme-ov-file#authentication

as this is a public repo, the k8s folder has no API_KEY set.
please edit k8s/3_2_scraper/0_scraper.secret.yaml and set the API_KEY in base64