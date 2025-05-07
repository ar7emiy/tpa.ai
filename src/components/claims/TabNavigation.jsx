// TabNavigation component 


import React from 'react';

const TabNavigation = ({ 
  primaryTabs, 
  secondaryTabs, 
  activePrimaryTab, 
  activeSecondaryTab, 
  setActivePrimaryTab, 
  setActiveSecondaryTab 
}) => {
  return (
    <>
      {/* Primary Tabs */}
      <div className="mx-4 mt-3">
        <div className="bg-gray-200 flex">
          {primaryTabs.map(tab => (
            <div 
              key={tab}
              className={`
                px-6 py-2 flex items-center justify-center cursor-pointer
                rounded-t-md
                ${activePrimaryTab === tab ? 'bg-blue-600 text-white font-bold' : 'bg-gray-200 text-gray-500'}
              `}
              onClick={() => setActivePrimaryTab(tab)}
            >
              <span className="text-sm">{tab}</span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Secondary Tabs */}
      <div className="mx-4">
        <div className="bg-blue-100 border border-blue-300 flex">
          {secondaryTabs.map(tab => (
            <div 
              key={tab}
              className={`
                px-6 py-1.5 flex items-center justify-center cursor-pointer
                ${activeSecondaryTab === tab ? 'bg-blue-200 text-blue-600 font-bold' : 'bg-blue-100 text-blue-600'}
              `}
              onClick={() => setActiveSecondaryTab(tab)}
            >
              <span className="text-xs">{tab}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default TabNavigation;