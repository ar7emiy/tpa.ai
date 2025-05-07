// FormProgressBar component 


import React from 'react';

const FormProgressBar = () => {
  return (
    <div className="mx-4 mb-1">
      <div className="relative h-1.5 bg-gray-200">
        <div className="absolute left-0 top-0 h-1.5 bg-blue-600 w-32"></div>
        <div className="absolute left-32 top-0 w-5 h-5 bg-blue-600 rounded-full -translate-y-1.5"></div>
      </div>
      
      <div className="flex justify-between text-xs text-gray-500 px-10">
        <div>Treatment Type</div>
        <div>Provider</div>
        <div>Dates</div>
        <div>Diagnosis</div>
        <div>Decision</div>
        <div>Notes</div>
        <div>Submit</div>
        <div>Return to Tasks</div>
      </div>
    </div>
  );
};

export default FormProgressBar;