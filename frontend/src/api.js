const API_BASE = 'http://localhost:8000';

/**
 * Upload a file to the backend.
 * @param {File} file
 * @returns {Promise<{file_id: string}>}
 */
export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

/**
 * Request analysis for a given file ID.
 * @param {string} fileId
 * @returns {Promise<any>}
 */
export async function analyzeFile(fileId) {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ file_id: fileId }),
  });
  if (!res.ok) throw new Error('Analysis failed');
  return res.json();
}

/**
 * Retrieve a previously computed analysis.
 * @param {string} fileId
 * @returns {Promise<any>}
 */
export async function getAnalysis(fileId) {
  const res = await fetch(`${API_BASE}/analysis/${fileId}`);
  if (!res.ok) throw new Error('Get analysis failed');
  return res.json();
}