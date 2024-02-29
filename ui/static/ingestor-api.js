
export class IngestorApi {
    /**
     * @returns {Promise<boolean>}
     */
    async checkIsDataIngested() {
      const response = await fetch('/ingestor/api/dataset', { method: 'GET' });
      return await response.json();
    }
  
    clearData() {
      return fetch('/ingestor/api/dataset', {method: 'DELETE'});
    }
  
    startDataIngestion() {
      return fetch('/ingestor/api/dataset/ingest', {method: 'POST'});
    }
  }