import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { fetchThought } from '../../api/apiService';
import LoadingSpinner from '../../components/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage';
import TagList from '../../components/TagList';
import ActionList from '../../components/ActionList';
import RelatedThoughts from '../../components/RelatedThoughts';
import { formatDate } from '../../utils/dateUtils';

export default function ThoughtDetail() {
  const router = useRouter();
  const { id } = router.query;
  
  const [thought, setThought] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      loadThought(id);
    }
  }, [id]);

  const loadThought = async (thoughtId) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchThought(thoughtId);
      setThought(data);
    } catch (err) {
      setError('Failed to load thought. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!id) {
    return null;
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      <Head>
        <title>{thought ? `${thought.content.substring(0, 30)}...` : 'Thought'} | Mirza Mirror</title>
        <meta name="description" content="View thought details in Mirza Mirror" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-neutral-900">Thought Details</h1>
            <button
              onClick={() => router.back()}
              className="text-neutral-600 hover:text-neutral-900"
            >
              Back
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {loading ? (
          <LoadingSpinner />
        ) : error ? (
          <ErrorMessage message={error} onRetry={() => loadThought(id)} />
        ) : thought ? (
          <div className="space-y-6">
            {/* Main content */}
            <div className="bg-white shadow-sm rounded-lg p-6">
              <p className="text-lg text-neutral-900 whitespace-pre-wrap">{thought.content}</p>
              
              <div className="mt-4 flex items-center text-sm text-neutral-500">
                <span>{formatDate(thought.createdAt)}</span>
                <span className="mx-2">•</span>
                <span>Source: {thought.source}</span>
              </div>
            </div>
            
            {/* Tags */}
            {thought.tags && thought.tags.length > 0 && (
              <div className="bg-white shadow-sm rounded-lg p-6">
                <h2 className="text-lg font-medium text-neutral-900 mb-4">Tags</h2>
                <TagList tags={thought.tags} />
              </div>
            )}
            
            {/* Summary */}
            {thought.summary && (
              <div className="bg-white shadow-sm rounded-lg p-6">
                <h2 className="text-lg font-medium text-neutral-900 mb-4">Summary</h2>
                <p className="text-neutral-700">{thought.summary}</p>
              </div>
            )}
            
            {/* Actions */}
            {thought.actions && thought.actions.length > 0 && (
              <div className="bg-white shadow-sm rounded-lg p-6">
                <h2 className="text-lg font-medium text-neutral-900 mb-4">Actions</h2>
                <ActionList actions={thought.actions} />
              </div>
            )}
            
            {/* Related Thoughts */}
            {thought.links && thought.links.length > 0 && (
              <div className="bg-white shadow-sm rounded-lg p-6">
                <h2 className="text-lg font-medium text-neutral-900 mb-4">Related Thoughts</h2>
                <RelatedThoughts links={thought.links} />
              </div>
            )}
            
            {/* Attachments */}
            {(thought.audioFile || thought.documentFile) && (
              <div className="bg-white shadow-sm rounded-lg p-6">
                <h2 className="text-lg font-medium text-neutral-900 mb-4">Attachments</h2>
                
                {thought.audioFile && (
                  <div className="mb-4 p-4 border border-neutral-200 rounded-md">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 text-primary-500">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-neutral-900">Audio Recording</h3>
                        <audio className="mt-2" controls src={thought.audioFile} />
                      </div>
                    </div>
                  </div>
                )}
                
                {thought.documentFile && (
                  <div className="p-4 border border-neutral-200 rounded-md">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 text-primary-500">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-neutral-900">
                          {thought.documentFile.split('/').pop()}
                        </h3>
                        <div className="mt-2">
                          <a
                            href={thought.documentFile}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-primary-600 hover:text-primary-500"
                          >
                            View Document
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ) : null}
      </main>
    </div>
  );
}
