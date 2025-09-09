import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import KeywordsList from './components/KeywordsList';
import SearchResults from './components/SearchResults';
import { analyseFile, analyseContent } from './services/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [clientName, setClientName] = useState('Chill.ie');
  const [campaignName, setCampaignName] = useState('The Counties With The Most Affordable Homes');
  const [campaignUrl, setCampaignUrl] = useState('https://www.chill.ie/the-counties-with-the-most-affordable-homes');

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Uploading file:', file.name);
      const data = await analyseFile(
        file,
        clientName,
        campaignName,
        campaignUrl        
      );
      console.log('Analysis complete:', data);
      setResults(data);
    } catch (err) {
      console.error('Error details:', err);
      
      // More specific error messages
      if (err.response) {
        // Server responded with error
        setError(`Server error: ${err.response.data.detail || 'Failed to analyse the file'}`);
      } else if (err.request) {
        // Request made but no response
        setError('Cannot connect to server. Make sure the backend is running on http://localhost:8000');
      } else {
        // Other errors
        setError('Failed to analyse the file. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleTextSubmit = async (text) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await analyseContent(
        text,
        clientName,
        campaignName,
        campaignUrl
      );
      setResults(data);
    } catch (err) {
      setError('Failed to analyse the content. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">
          Link Dive MVP - PR Coverage Finder
        </h1>
        
        <div className="max-w-2xl mx-auto mb-8">
          {/* Custom client/campaign inputs */}
          <div className="mb-4 space-y-2">
            <label className="block text-sm font-medium text-gray-700">Client Name</label>
            <input
              type="text"
              className="w-full p-2 border rounded"
              placeholder="Client Name (default: Chill.ie)"
              value={clientName}
              onChange={(e) => setClientName(e.target.value)}
            />
            <label className="block text-sm font-medium text-gray-700">Campaign Name</label>
            <input
              type="text"
              className="w-full p-2 border rounded"
              placeholder="Campaign Name (optional)"
              value={campaignName}
              onChange={(e) => setCampaignName(e.target.value)}
            />
            <label className="block text-sm font-medium text-gray-700">Campaign URL</label>
            <input
              type="text"
              className="w-full p-2 border rounded"
              placeholder="Campaign URL (optional)"
              value={campaignUrl}
              onChange={(e) => setCampaignUrl(e.target.value)}
            />
          </div>
          <FileUploader onFileUpload={handleFileUpload} />
          
          <div className="mt-4">
            <p className="text-center text-gray-600 mb-2">OR</p>
            <textarea
              className="w-full p-4 border rounded-lg"
              rows="6"
              placeholder="Paste your landing page copy here..."
              onBlur={(e) => {
                if (e.target.value) {
                  handleTextSubmit(e.target.value);
                }
              }}
            />
          </div>
        </div>

        {loading && (
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2">Analysing content...</p>
          </div>
        )}

        {error && (
          <div className="max-w-2xl mx-auto mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {results && (
          <div className="grid md:grid-cols-2 gap-6 max-w-6xl mx-auto">
            <KeywordsList
              keywords={results.suggested_keywords}
              selectedKeyword={results.selected_keyword}
            />
            <SearchResults
              results={results.serp_results}
              keyword={results.selected_keyword}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;