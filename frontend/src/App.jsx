import React, { useState } from 'react';
import { uploadFile, analyzeFile, getAnalysis } from './api.js';

export default function App() {
  const [file, setFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    try {
      const { file_id } = await uploadFile(file);
      setFileId(file_id);
      const analysis = await analyzeFile(file_id);
      setResult(analysis);
    } catch (err) {
      console.error(err);
      alert('Upload or analysis failed');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-8">
      <h1 className="text-2xl font-bold mb-4">AI Compliance MVP</h1>
      <form onSubmit={handleUpload} className="w-full max-w-md bg-white p-6 rounded-lg shadow">
        <label className="block mb-2 font-medium">Select a document</label>
        <input
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-4 w-full"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Upload & Analyze'}
        </button>
      </form>
      {result && (
        <div className="mt-8 w-full max-w-2xl bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">Analysis Result</h2>
          <p className="mb-1"><strong>File ID:</strong> {result.file_id}</p>
          <p className="mb-1"><strong>Risk Score:</strong> {result.risk_score.toFixed(2)}</p>
          {result.details && result.details.flagged_terms && (
            <p className="mb-1"><strong>Flagged Terms:</strong> {result.details.flagged_terms.length > 0 ? result.details.flagged_terms.join(', ') : 'None'}</p>
          )}
          <pre className="whitespace-pre-wrap bg-gray-100 p-3 rounded mb-2">
            {result.summary}
          </pre>
          {result.details && result.details.recommendations && (
            <p className="text-sm text-gray-700"><strong>Recommendation:</strong> {result.details.recommendations}</p>
          )}
        </div>
      )}
    </div>
  );
}