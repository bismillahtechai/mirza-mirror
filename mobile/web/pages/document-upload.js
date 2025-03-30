import React, { useState, useRef } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { uploadDocument } from '../api/apiService';

const DocumentUpload = () => {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
    }
  };
  
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setSelectedFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };
  
  const handleUpload = async () => {
    if (!selectedFile) return;
    
    try {
      setIsUploading(true);
      setError(null);
      
      await uploadDocument(selectedFile);
      router.push('/');
      
    } catch (err) {
      console.error('Error uploading document:', err);
      setError('Failed to upload document. Please try again.');
      setIsUploading(false);
    }
  };
  
  const getFileIcon = () => {
    if (!selectedFile) return null;
    
    const fileType = selectedFile.type;
    
    if (fileType.includes('image')) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      );
    } else if (fileType.includes('pdf')) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      );
    } else if (fileType.includes('word') || fileType.includes('document')) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      );
    } else {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      );
    }
  };
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Head>
        <title>Document Upload | Mirza Mirror</title>
        <meta name="description" content="Upload a document to Mirza Mirror" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-neutral-900">Document Upload</h1>
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
        <div className="bg-white shadow-sm rounded-lg p-6">
          {error && (
            <div className="mb-6 p-3 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}
          
          <div 
            className="border-2 border-dashed border-neutral-300 rounded-lg p-12 text-center cursor-pointer hover:border-primary-500 transition-colors"
            onClick={() => fileInputRef.current?.click()}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <input 
              type="file" 
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
              accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
            />
            
            {selectedFile ? (
              <div className="flex flex-col items-center">
                <div className="text-primary-500 mb-4">
                  {getFileIcon()}
                </div>
                <p className="text-lg font-medium text-neutral-900 mb-2">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-neutral-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedFile(null);
                  }}
                  className="mt-4 text-sm text-primary-600 hover:text-primary-800"
                >
                  Change file
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <div className="text-neutral-400 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <p className="text-lg font-medium text-neutral-900 mb-2">
                  Drag and drop a file here, or click to select
                </p>
                <p className="text-sm text-neutral-500">
                  Supports PDF, Word, text files, and images
                </p>
              </div>
            )}
          </div>
          
          <div className="mt-6 flex justify-end">
            <button
              onClick={handleUpload}
              disabled={!selectedFile || isUploading}
              className={`px-4 py-2 rounded-md text-white ${
                !selectedFile || isUploading
                  ? 'bg-primary-300 cursor-not-allowed'
                  : 'bg-primary-600 hover:bg-primary-700'
              } transition-colors`}
            >
              {isUploading ? 'Uploading...' : 'Upload Document'}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DocumentUpload;
