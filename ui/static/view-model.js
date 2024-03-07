import { AnalyticsApi } from './analytics-api.js';
import {IngestorApi} from './ingestor-api.js';
import {ScraperApi} from './scraper-api.js';

const ingestApi = new IngestorApi();
const analyticsApi = new AnalyticsApi();
const scraperApi = new ScraperApi();

export class DataIngestionViewModel extends EventTarget {
    #dataIngested = false;
    allowAnalytics = false;

    /** @type {string} */
    #selectedReport = null;

    #reportData = null;

    #setDataIngested(value) {
        this.#dataIngested = value;
        this.#setAllowAnalytics(value);
        this.dispatchEvent(new CustomEvent('dataIngestedChange', {detail: value}))
    }

    #setAllowAnalytics(value) {
        this.allowAnalytics = value;
        this.dispatchEvent(new CustomEvent('allowAnalytics', {detail: value}));
    }
    

    get dataIngested() {
        return this.#dataIngested;
    }

    async checkIsDataIngested() {
        const result = await ingestApi.checkIsDataIngested();
        this.#setDataIngested(result);
    }

    async clearData() {
        await ingestApi.clearData();
        this.#setDataIngested(false);
    }

    async startDataIngestion() {
        this.dispatchEvent(new CustomEvent('dataIngestionStart'));
        await ingestApi.startDataIngestion();
        this.#setDataIngested(true);
    }
    
    async selectReport(reportName) {
        this.#selectedReport = reportName;
        this.#reportData = await analyticsApi.getReport(reportName);
        this.dispatchEvent(new CustomEvent('reportResult', {detail: this.#reportData}));
    }

    async scrapeData(phrases, limit) {
        if (!phrases || !limit) {
            console.error('Phrases and limit are required');
            return;
        }
        this.dispatchEvent(new CustomEvent('dataIngestionStart'));
        await scraperApi.startDataScraping(phrases, limit);
        this.#setDataIngested(true);
    }
}
