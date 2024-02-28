const ingestButton = document.getElementById('ingest-button');
const reportSelect = document.getElementById('report-select');
const imageContainer = document.getElementById('image-container');

let dataIngested = false;

ingestButton.addEventListener('click', () => {
  dataIngested = true;
  reportSelect.disabled = false;
});

reportSelect.addEventListener('change', async () => {
  if (!dataIngested) {
    alert('Please initiate data ingestion first!');
    return;
  }

  const reportName = reportSelect.value;
  const response = await fetch(`/api/report/${reportName}`);

  if (!response.ok) {
    alert(`Error fetching report: ${response.statusText}`);
    return;
  }

  const blob = await response.blob();
  const imageUrl = URL.createObjectURL(blob);

  const image = document.createElement('img');
  image.src = imageUrl;

  imageContainer.innerHTML = '';
  imageContainer.appendChild(image);
});
