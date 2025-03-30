import React, { useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { createThought } from '../api/apiService';

export default function AddThought() {
  const router = useRouter();
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!content.trim()) {
      return;
    }
    
    try {
      setIsSubmitting(true);
      setError(null);
      await createThought(content);
      router.push('/');
    } catch (err) {
      setError('Failed to save thought. Please try again.');
      console.error(err);
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <Head>
        <title>Add Thought | Mirza Mirror</title>
        <meta name="description" content="Add a new thought to Mirza Mirror" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-neutral-900">Add Thought</h1>
            <button
              onClick={() => router.back()}
              className="text-neutral-600 hover:text-neutral-900"
            >
              Cancel
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <form onSubmit={handleSubmit} className="bg-white shadow-sm rounded-lg p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}
          
          <div className="mb-4">
            <label htmlFor="content" className="block text-sm font-medium text-neutral-700 mb-1">
              Your Thought
            </label>
            <textarea
              id="content"
              name="content"
              rows={8}
              className="w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="What's on your mind?"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              disabled={isSubmitting}
            />
          </div>
          
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isSubmitting || !content.trim()}
              className={`px-4 py-2 rounded-md text-white ${
                isSubmitting || !content.trim()
                  ? 'bg-primary-300 cursor-not-allowed'
                  : 'bg-primary-600 hover:bg-primary-700'
              } transition-colors`}
            >
              {isSubmitting ? 'Saving...' : 'Save Thought'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
