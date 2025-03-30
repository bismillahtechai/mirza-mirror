import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { fetchThoughts, searchThoughts } from '../api/apiService';
import ThoughtCard from '../components/ThoughtCard';
import SearchBar from '../components/SearchBar';
import AddButton from '../components/AddButton';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

export default function Home() {
  const router = useRouter();
  const [thoughts, setThoughts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadThoughts();
  }, []);

  const loadThoughts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchThoughts();
      setThoughts(data);
    } catch (err) {
      setError('Failed to load thoughts. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (!query.trim()) {
      loadThoughts();
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await searchThoughts(query);
      setThoughts(data);
    } catch (err) {
      setError('Search failed. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddThought = () => {
    router.push('/add-thought');
  };

  const handleThoughtClick = (id) => {
    router.push(`/thoughts/${id}`);
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <Head>
        <title>Mirza Mirror</title>
        <meta name="description" content="Externalize and organize your thoughts" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-neutral-900">Mirza Mirror</h1>
            <SearchBar onSearch={handleSearch} />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {loading ? (
          <LoadingSpinner />
        ) : error ? (
          <ErrorMessage message={error} onRetry={loadThoughts} />
        ) : thoughts.length === 0 ? (
          <div className="text-center py-12">
            <h2 className="text-xl font-medium text-neutral-600">No thoughts found</h2>
            {searchQuery ? (
              <p className="mt-2 text-neutral-500">
                No results for "{searchQuery}". Try a different search term.
              </p>
            ) : (
              <p className="mt-2 text-neutral-500">
                Start by adding your first thought.
              </p>
            )}
            <button
              onClick={handleAddThought}
              className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
            >
              Add Your First Thought
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {thoughts.map((thought) => (
              <ThoughtCard
                key={thought.id}
                thought={thought}
                onClick={() => handleThoughtClick(thought.id)}
              />
            ))}
          </div>
        )}
      </main>

      <AddButton onClick={handleAddThought} />
    </div>
  );
}
