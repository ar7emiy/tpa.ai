// ClaimHeader component 

import React from 'react';

const ClaimHeader = ({ claimData }) => {
  return (
    <div className="mx-4 mt-2">
      <div className="bg-gray-100 border rounded-md p-4">
        <div className="flex justify-between">
          <div>
            <div className="text-gray-500 text-xs">Claim #: {claimData.claimNumber}</div>
            <div className="text-gray-900 font-bold text-sm mt-1">
              {claimData.claimant} - {claimData.injury} ({claimData.injuryDate})
            </div>
          </div>
          
          <div>
            <div className="text-gray-500 text-xs">Employer: {claimData.employer}</div>
            <div className="text-gray-500 text-xs mt-1">Assigned Adjuster: {claimData.adjuster}</div>
          </div>
          
          <div>
            <div className="text-gray-500 text-xs">Status: {claimData.status}</div>
            <div className="text-gray-500 text-xs mt-1">State: {claimData.state}</div>
          </div>
          
          {claimData.hasDueTask && (
            <div className="bg-red-600 text-white px-6 py-1 rounded flex items-center text-sm font-bold">
              TASK DUE TODAY: {claimData.dueTaskName}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClaimHeader;