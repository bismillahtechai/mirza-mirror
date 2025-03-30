import React from 'react';

const AddButton = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-primary-600 text-white shadow-lg flex items-center justify-center hover:bg-primary-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      aria-label="Add thought"
    >
      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
      </svg>
    </button>
  );
};

export default AddButton;
