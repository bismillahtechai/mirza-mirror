import React from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <input
        type="text"
        placeholder="Search thoughts..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full md:w-64 px-4 py-2 pr-10 rounded-md border border-neutral-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      />
      <button
        type="submit"
        className="absolute inset-y-0 right-0 flex items-center px-3 text-neutral-500"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>
    </form>
  );
};

export default SearchBar;
