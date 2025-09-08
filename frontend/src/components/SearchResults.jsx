const SearchResults = ({ results, keyword }) => {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-2">Search Results</h2>
        <p className="text-sm text-gray-600 mb-4">For keyword: "{keyword}"</p>
        <div className="space-y-4">
          {results.map((result) => (
            <div key={result.position} className="border-b pb-3">
              <div className="flex items-start">
                <span className="text-sm text-gray-500 mr-3">#{result.position}</span>
                <div className="flex-1">
                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline font-medium"
                  >
                    {result.title}
                  </a>
                  <p className="text-sm text-gray-600 mt-1">{result.description}</p>
                  <p className="text-xs text-green-600 mt-1">{result.url}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  export default SearchResults;