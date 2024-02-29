
export class AnalyticsApi {
    /**
     * @param {string} reportName 
     * @returns {Promise<string>}
     */
    async getReport(reportName) {
        const response = await fetch(`/analytics/api/${reportName}/image`);
        if (!response.ok) {
            console.error(`Error fetching report: ${response.statusText}`);
            return;
          }
        
          const blob = await response.blob();
          const imageUrl = URL.createObjectURL(blob);
          return imageUrl;
    }
  
  }