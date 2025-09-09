const KeywordsList = ({ keywords, selectedKeyword }) => {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Suggested Keywords</h2>
        <ul className="space-y-2">
          {keywords.map((keyword, index) => (
            <li
              key={index}
              className={`p-2 rounded ${
                keyword === selectedKeyword
                  ? 'bg-blue-100 border-blue-300 border'
                  : 'bg-gray-50'
              }`}
            >
              {keyword}
              {keyword === selectedKeyword && (
                <span className="ml-2 text-sm text-blue-600">(Analysed)</span>
              )}
            </li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default KeywordsList;