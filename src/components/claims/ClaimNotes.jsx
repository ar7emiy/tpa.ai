// ClaimNotes component 


import React from 'react';

const ClaimNotes = ({ notes, aiRecommendation }) => {
  return (
    <div className="w-1/3 bg-gray-100 border rounded-md">
      <div className="p-4">
        <h2 className="font-bold text-sm">Claim Notes &amp; Sources</h2>
        
        {/* Notes */}
        <div className="mt-3 space-y-3">
          {notes.map(note => (
            <div key={note.id} className="bg-white border rounded-md p-2">
              <div className="font-bold text-xs">{note.title}</div>
              <div className="text-gray-500 text-xs mt-0.5">{note.source}</div>
              <div className="text-xs mt-2">{note.content}</div>
            </div>
          ))}
        </div>
        
        {/* AI Recommendation */}
        <div className="mt-3 bg-blue-50 border border-blue-300 rounded-md p-2">
          <div className="font-bold text-xs text-blue-600">{aiRecommendation.title}</div>
          <div className="text-xs mt-1">{aiRecommendation.content}</div>
        </div>
      </div>
    </div>
  );
};

export default ClaimNotes;