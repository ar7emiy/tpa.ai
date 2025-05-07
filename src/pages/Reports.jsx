// Reports page component 


import React, { useState } from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';

// This would normally be imported from data files
import { mockUser } from '../data/mockData';

const Reports = () => {
  const [activeTab, setActiveTab] = useState("Reports");
  
  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <Header 
        user={mockUser} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
      />
      
      {/* Main Content */}
      <div className="flex-1 p-4">
        <h1 className="text-2xl font-bold mb-4">Reports</h1>
        <p className="text-gray-600">Reports dashboard will be implemented here.</p>
        
        {/* Placeholder for Reports content */}
        <div className="mt-4 p-8 bg-white border rounded-md flex items-center justify-center text-gray-400">
          Reports content coming soon
        </div>
      </div>
      
      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Reports;