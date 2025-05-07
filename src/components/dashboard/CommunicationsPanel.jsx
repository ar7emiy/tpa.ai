// CommunicationsPanel component 

import React, { useState } from 'react';
import CommunicationItem from './CommunicationItem';

const CommunicationsPanel = ({ communications, selectedCommunication, setSelectedCommunication }) => {
  const [activeFilter, setActiveFilter] = useState("All");
  const filters = ["All", "Email", "Phone", "Fax", "Notes"];
  
  return (
    <div className="w-1/2 border-r">
      {/* Panel Header */}
      <div className="bg-gray-200 h-12 flex items-center justify-between px-4">
        <h2 className="font-bold text-gray-800">Communications</h2>
        
        {/* Search Bar */}
        <div className="flex">
          <input 
            type="text" 
            placeholder="Search messages..." 
            className="px-2 py-1 text-xs border rounded-l w-56"
          />
          <button className="bg-blue-600 text-white px-4 py-1 text-xs rounded-r">
            Search
          </button>
        </div>
      </div>
      
      {/* Filter Tabs */}
      <div className="flex px-4 pt-4 gap-2">
        {filters.map(filter => (
          <div 
            key={filter}
            className={`px-4 py-1.5 text-xs rounded cursor-pointer ${
              activeFilter === filter 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-800'
            }`}
            onClick={() => setActiveFilter(filter)}
          >
            {filter}
          </div>
        ))}
      </div>
      
      {/* Communications List */}
      <div className="overflow-y-auto mt-2 px-4 pb-4 h-[calc(100%-120px)]">
        {communications.map(comm => (
          <CommunicationItem 
            key={comm.id}
            comm={comm}
            isSelected={selectedCommunication === comm.id}
            onClick={() => setSelectedCommunication(comm.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default CommunicationsPanel;