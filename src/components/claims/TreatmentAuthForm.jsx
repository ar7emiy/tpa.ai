// TreatmentAuthForm component 


import React from 'react';

const TreatmentAuthForm = ({ formData, handleInputChange, handleSubmit }) => {
  return (
    <div className="w-2/3 border rounded-md mr-2">
      <div className="p-4">
        <h1 className="text-gray-900 font-bold text-base">Medical Treatment Authorization</h1>
        
        <div className="mt-2 border border-gray-200 rounded-md p-4">
          {/* Treatment Information */}
          <div className="font-bold text-sm">Treatment Information</div>
          
          <div className="grid grid-cols-2 gap-4 mt-2">
            <div>
              <label className="text-xs text-gray-500 block">Treatment Type</label>
              <div className="bg-blue-50 border border-blue-300 rounded px-2 py-1.5 text-xs mt-1">
                {formData.type}
              </div>
              <div className="text-xs text-blue-600 mt-0.5">From: Email, Dr. Sarah Williams</div>
            </div>
            
            <div>
              <label className="text-xs text-gray-500 block">Provider</label>
              <div className="bg-yellow-50 border border-yellow-300 rounded px-2 py-1.5 text-xs mt-1">
                {formData.provider}
              </div>
              <div className="text-xs text-blue-600 mt-0.5">From: Email, Dr. Sarah Williams</div>
            </div>
          </div>
          
          <div className="grid grid-cols-4 gap-4 mt-4">
            <div>
              <label className="text-xs text-gray-500 block">Start Date</label>
              <input 
                type="text" 
                value={formData.startDate}
                onChange={(e) => handleInputChange("startDate", e.target.value)}
                className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-full"
              />
            </div>
            
            <div>
              <label className="text-xs text-gray-500 block">End Date</label>
              <input 
                type="text" 
                value={formData.endDate}
                onChange={(e) => handleInputChange("endDate", e.target.value)}
                className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-full"
              />
            </div>
            
            <div>
              <label className="text-xs text-gray-500 block">Frequency</label>
              <input 
                type="text" 
                value={formData.frequency}
                onChange={(e) => handleInputChange("frequency", e.target.value)}
                className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-full"
              />
            </div>
            
            <div>
              <label className="text-xs text-gray-500 block">Sessions</label>
              <input 
                type="text" 
                value={formData.sessions}
                onChange={(e) => handleInputChange("sessions", e.target.value)}
                className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-full"
              />
            </div>
          </div>
          
          {/* Diagnosis Information */}
          <div className="font-bold text-sm mt-6">Diagnosis Information</div>
          
          <div className="grid grid-cols-1 gap-4 mt-2">
            <div>
              <label className="text-xs text-gray-500 block">Primary Diagnosis</label>
              <div className="flex">
                <input 
                  type="text" 
                  value={formData.primaryDiagnosis}
                  onChange={(e) => handleInputChange("primaryDiagnosis", e.target.value)}
                  className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-3/5"
                />
                <div className="text-xs text-blue-600 mt-3 ml-2">From: Fax, Memorial Hospital</div>
              </div>
            </div>
            
            <div>
              <label className="text-xs text-gray-500 block">Secondary Diagnosis</label>
              <div className="flex">
                <input 
                  type="text" 
                  value={formData.secondaryDiagnosis}
                  onChange={(e) => handleInputChange("secondaryDiagnosis", e.target.value)}
                  className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-3/5"
                />
                <div className="text-xs text-blue-600 mt-3 ml-2">From: Fax, Memorial Hospital</div>
              </div>
            </div>
          </div>
          
          {/* Authorization Decision */}
          <div className="font-bold text-sm mt-6">Authorization Decision</div>
          
          <div className="grid grid-cols-2 gap-4 mt-2">
            <div>
              <label className="text-xs text-gray-500 block">Decision</label>
              <select
                value={formData.decision}
                onChange={(e) => handleInputChange("decision", e.target.value)}
                className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-full"
              >
                <option>Approved</option>
                <option>Denied</option>
                <option>Pending</option>
              </select>
            </div>
            
            <div>
              <label className="text-xs text-gray-500 block">Authorization Code</label>
              <input 
                type="text" 
                value={formData.authCode}
                onChange={(e) => handleInputChange("authCode", e.target.value)}
                className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-full"
              />
            </div>
          </div>
          
          <div className="mt-4">
            <label className="text-xs text-gray-500 block">Notes</label>
            <textarea
              value={formData.notes}
              onChange={(e) => handleInputChange("notes", e.target.value)}
              className="border border-gray-300 rounded px-2 py-1.5 text-xs mt-1 w-full h-16 resize-none"
            />
          </div>
          
          {/* Action Buttons */}
          <div className="mt-6 flex items-center gap-4">
            <button 
              onClick={handleSubmit}
              className="bg-blue-600 text-white px-6 py-2 rounded text-sm"
            >
              Submit
            </button>
            
            <button 
              className="bg-gray-500 text-white px-6 py-2 rounded text-sm"
            >
              Cancel
            </button>
            
            <button 
              className="bg-green-600 text-white px-6 py-2 rounded text-sm"
            >
              Generate Auth Letter
            </button>
            
            {/* Tab progression guidance */}
            <div className="ml-auto bg-yellow-100 border border-yellow-400 rounded px-4 py-2 text-xs text-gray-700">
              Press TAB to move to Provider field
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TreatmentAuthForm;