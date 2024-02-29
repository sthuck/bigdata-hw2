//@ts-check

import { DataIngestionViewModel } from './view-model.js';


const vm = new DataIngestionViewModel();
/** @type {HTMLButtonElement | null} */
// @ts-ignore
const ingestButton = document.getElementById('ingest-button');

/** @type {HTMLButtonElement | null} */
// @ts-ignore
const clearButton = document.getElementById('clear-button');

/** @type {HTMLSelectElement | null} */
// @ts-ignore
const reportSelect = document.getElementById('report-select');
const imageContainer = document.getElementById('image-container');

if (!ingestButton || !reportSelect || !imageContainer) {
  throw new Error('Missing required elements');
}

window.addEventListener('load', () => vm.checkIsDataIngested())

ingestButton.addEventListener('click', () => vm.startDataIngestion());
reportSelect.addEventListener('change', () => vm.selectReport(reportSelect.value));
clearButton.addEventListener('click', () => vm.clearData());

vm.addEventListener('dataIngestedChange',
  /**
   * @param {CustomEvent} event
   */
  (event) => {
    ingestButton.disabled = event.detail;
    ingestButton.textContent = event.detail ? 'Data already ingested' : 'Ingest Data';
    ingestButton.classList.remove('is-loading');
  });

  vm.addEventListener('dataIngestionStart',
  () => {
    ingestButton.disabled = true;
    ingestButton.classList.add('is-loading');
  });

vm.addEventListener('allowAnalytics',
  /**
   * @param {CustomEvent} event
   */
  (event) => {
    reportSelect.disabled = !event.detail;
  })


vm.addEventListener('reportResult',
  /**
   * @param {CustomEvent} event
   */
  async (event) => {
    const image = document.createElement('img');
    image.src = event.detail;

    imageContainer.innerHTML = '';
    imageContainer.appendChild(image);
  });
