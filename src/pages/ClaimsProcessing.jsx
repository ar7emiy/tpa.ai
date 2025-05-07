// ClaimsProcessing page component 

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ClaimHeader from '../components/claims/ClaimHeader';
import TabNavigation from '../components/claims/TabNavigation';
import TreatmentAuthForm from '../components/claims/TreatmentAuthForm';
import ClaimNotes from '../components/claims/ClaimNotes';
import FormProgressBar from '../components/claims/FormProgressBar';

// This would normally be imported from data files
import { mockUser, mockClaimData, mockTasks } from '../data/mockData';

const ClaimsProcessing = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeNavTab, setActiveNavTab] = useState("Claims");
  const [activePrimaryTab, setActivePrimaryTab] = useState("Medical");
  const [activeSecondaryTab, setActiveSecondaryTab] = useState("Treatment Auth");
  const [formData, setFormData] = useState(mockClaimData.treatment);
  const [taskData, setTaskData] = useState(null);
  
  // Fetch the task data based on the ID from the URL
  useEffect(() => {
    // In a real app, you would fetch this data from an API
    // For now, we'll use the mock data
    if (id) {
      const task = mockTasks.find(task => task.id.toString() === id.toString());
      if (task) {
        setTaskData(task);
      } else {
        console.error(`Task with ID ${id} not found`);
        // Optionally redirect back to dashboard if task not found
        // navigate('/dashboard');
      }
    }
  }, [id, navigate]);
  
  // Handle back button click
  const handleBackToDashboard = () => {
    navigate('/dashboard');
  };
  
  // Tabs data
  const primaryTabs = ["Medical", "Indemnity", "Notes", "Documents", "Financials"];
  const secondaryTabs = ["Treatment Auth", "Medical History", "Providers", "Rx Management"];
  
  // Handle form submission
  const handleSubmit = () => {
    console.log("Form submitted:", formData);
    // In a real app, you would save the data to your backend here
    alert("Form submitted successfully!");
  };
  
  // Handle form input changes
  const handleInputChange = (field, value) => {
    setFormData({
      ...formData,
      [field]: value
    });
  };
  
  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <Header 
        user={mockUser} 
        activeTab={activeNavTab} 
        setActiveTab={setActiveNavTab} 
      />
      
      {/* Breadcrumb */}
      <div className="bg-gray-200 px-4 py-1.5 flex items-center">
        <button 
          onClick={handleBackToDashboard}
          className="text-blue-600 text-xs mr-2 hover:underline"
        >
          &lt; Back to Dashboard
        </button>
        <span className="text-xs text-gray-500">
          Dashboard &gt; Claims &gt; {mockClaimData.claimNumber} &gt; Medical Treatment Authorization
          {taskData && ` (Task: ${taskData.title})`}
        </span>
      </div>
      
      {/* Claim Header */}
      <ClaimHeader claimData={mockClaimData} />
      
      {/* Tab Navigation */}
      <TabNavigation 
        primaryTabs={primaryTabs}
        secondaryTabs={secondaryTabs}
        activePrimaryTab={activePrimaryTab}
        activeSecondaryTab={activeSecondaryTab}
        setActivePrimaryTab={setActivePrimaryTab}
        setActiveSecondaryTab={setActiveSecondaryTab}
      />
      
      {/* Main Content Area */}
      <div className="flex mx-4 mt-2 mb-4 flex-1">
        {/* Left side - Form */}
        <TreatmentAuthForm 
          formData={formData}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
        />
        
        {/* Right side - Claim notes and sources */}
        <ClaimNotes 
          notes={mockClaimData.notes}
          aiRecommendation={mockClaimData.aiRecommendation}
        />
      </div>
      
      {/* Tab progression visualization */}
      <FormProgressBar />
      
      {/* Footer */}
      <Footer />
    </div>
  );
};

export default ClaimsProcessing;