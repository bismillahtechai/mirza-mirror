import React from 'react';
import { formatRelativeDate } from '../utils/dateUtils';

const ThoughtCard = ({ thought, onClick }) => {
  return (
    <div 
      className="bg-white shadow-sm rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
      onClick={onClick}
    >
      <p className="text-neutral-900 line-clamp-3">{thought.content}</p>
      
      <div className="mt-3 flex justify-between items-center">
        <span className="text-sm text-neutral-500">
          {formatRelativeDate(thought.createdAt)}
        </span>
        
        {thought.tags && thought.tags.length > 0 && (
          <div className="flex space-x-1">
            {thought.tags.slice(0, 2).map((tag) => (
              <span 
                key={tag.id}
                className="inline-block px-2 py-0.5 text-xs rounded-full bg-primary-100 text-primary-800"
              >
                {tag.name}
              </span>
            ))}
            {thought.tags.length > 2 && (
              <span className="inline-block px-2 py-0.5 text-xs rounded-full bg-neutral-100 text-neutral-800">
                +{thought.tags.length - 2}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ThoughtCard;
