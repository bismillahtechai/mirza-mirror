import React from 'react';

const ActionList = ({ actions }) => {
  if (!actions || actions.length === 0) {
    return null;
  }

  return (
    <div className="space-y-3">
      {actions.map((action) => (
        <div 
          key={action.id} 
          className="flex items-start p-3 border border-neutral-200 rounded-md"
        >
          <input
            type="checkbox"
            checked={action.completed}
            onChange={() => {/* Handle checkbox change */}}
            className="h-5 w-5 text-primary-600 rounded border-neutral-300 focus:ring-primary-500 mt-0.5"
          />
          
          <div className="ml-3 flex-1">
            <p className={`text-neutral-900 ${action.completed ? 'line-through text-neutral-500' : ''}`}>
              {action.content}
            </p>
            
            <div className="mt-1 flex items-center space-x-2">
              {action.priority && (
                <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                  action.priority.toLowerCase() === 'high' 
                    ? 'bg-red-100 text-red-800' 
                    : action.priority.toLowerCase() === 'medium'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-blue-100 text-blue-800'
                }`}>
                  {action.priority}
                </span>
              )}
              
              {action.dueDate && (
                <span className="text-xs text-neutral-500">
                  Due: {new Date(action.dueDate).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ActionList;
