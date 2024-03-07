
export class ScraperApi {
    startDataScraping(phrases, limit) {
      return fetch('/scraper/ingest', 
      {method: 'POST', body: JSON.stringify({phrases, limit}), headers: {'Content-Type': 'application/json'}});
    }
  }