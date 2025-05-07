// CommunicationItem component 

import React from 'react';

const CommunicationItem = ({ comm, isSelected, onClick }) => {
  return (
    <div 
      className={`border-t border-x first:border-t p-3 cursor-pointer ${
        comm.id === 1 ? 'bg-gray-100' : 'bg-white'
      } ${isSelected ? 'ring-2 ring-blue-500' : ''}`}
      onClick={onClick}
    >
      <div className="flex">
        {/* Icon */}
        <div 
          className="w-6 h-6 rounded-full flex items-center justify-center text-white text-xs"
          style={{ backgroundColor: comm.iconColor }}
        >
          {comm.icon}
        </div>
        
        {/* Content */}
        <div className="ml-2 flex-1">
          <div className="font-bold text-sm">{`${comm.type.charAt(0).toUpperCase() + comm.type.slice(1)} from: ${comm.from}`}</div>
          <div className="text-sm mt-0.5">{`${comm.type === 'email' ? 'Subject' : 'Topic'}: ${comm.subject}`}</div>
          <div className="text-xs text-gray-500 mt-1">{comm.preview}</div>
          <div className="text-xs text-gray-500 mt-2">{comm.date}</div>
        </div>
        
        {/* New Badge */}
        {comm.isNew && (
          <div className="bg-red-600 text-white text-xs px-2 py-0.5 rounded-full flex items-center h-4">
            NEW
          </div>
        )}
      </div>
    </div>
  );
};

export default CommunicationItem;