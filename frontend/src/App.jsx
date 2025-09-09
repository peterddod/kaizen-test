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
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = (file) => {
    setSelectedFile(file);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select a file to analyse.');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      let data;
      if (selectedFile) {
        console.log('Uploading file:', selectedFile.name);
        data = await analyseFile(
          selectedFile,
          clientName,
          campaignName,
          campaignUrl        
        );
      }
      console.log('Analysis complete:', data);
      setResults(data);
    } catch (err) {
      console.error('Error details:', err);
      
      // More specific error messages
      if (err.response) {
        // Server responded with error
        setError(`Server error: ${err.response.data.detail || 'Failed to analyse the content'}`);
      } else if (err.request) {
        // Request made but no response
        setError('Cannot connect to server. Make sure the backend is running on http://localhost:8000');
      } else {
        // Other errors
        setError('Failed to analyse the content. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 font-inter">
      <div className='flex flex-col'>
        <h1 className="text-3xl font-bold mb-4 text-white bg-black py-4 pl-4 text-left">
          Link Dive MVP - PR Coverage Finder
        </h1>
        
        <div className="w-full 2xl:w-[1500px] mb-8 flex flex-col p-8 mx-auto border-b border-gray-300">
            {/* Custom client/campaign inputs */}
            <div className="flex flex-col lg:flex-row gap-8">
                <div className="mb-4 space-y-2 w-full lg:w-1/2">
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

                <div className="w-full lg:w-1/2 my-auto">
                    <FileUploader onFileUpload={handleFileUpload} />
                </div>
            </div>
            {/* Submit Button */}
            <div className="w-full lg:w-[600px] mt-8 mx-auto font-bebas text-2xl">
                <button
                onClick={handleSubmit}
                disabled={loading || (!selectedFile)}
                className={`w-full py-3 px-4 rounded-lg font-medium ${
                    loading || (!selectedFile)
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-green text-white hover:bg-green/80'
                } transition-colors`}
                >
                {loading ? 'Analysing...' : 'Analyse Content'}
                </button>
            </div>
        </div>

        {loading && (
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2">Analysing content...</p>
          </div>
        )}

        {error && (
          <div className="max-w-2xl mx-auto mb-4 p-4 bg-red-100 text-red-700 rounded-lg mx-8">
            {error}
          </div>
        )}

        {results && (
          <div className="w-full 2xl:w-[1500px] mx-auto flex flex-col gap-8 lg:flex-row px-8 mb-8">
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