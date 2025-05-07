// Dashboard page component 

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import CommunicationsPanel from '../components/dashboard/CommunicationsPanel';
import TasksPanel from '../components/dashboard/TasksPanel';

// This would normally be imported from data files
import { mockUser, mockCommunications, mockTasks, mockStats } from '../data/mockData';

const Dashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("Dashboard");
  const [selectedCommunication, setSelectedCommunication] = useState(null);
  const [selectedTask, setSelectedTask] = useState(null);
  
  // Handle tab key navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Tab' && selectedTask) {
        e.preventDefault();
        // Navigate to the claims page with the selected task ID
        navigate(`/claims/${selectedTask}`);
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedTask, navigate]);
  
  // Handle task click
  const handleTaskClick = (taskId) => {
    setSelectedTask(taskId);
    // Double-click (or you could add a specific button) to navigate
    if (selectedTask === taskId) {
      navigate(`/claims/${taskId}`);
    }
  };
  
  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <Header 
        user={mockUser} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
      />
      
      {/* Main Content */}
      <div className="flex-1 p-2 overflow-hidden">
        <div className="bg-white border rounded h-full flex">
          {/* Left Panel - Communications */}
          <CommunicationsPanel 
            communications={mockCommunications} 
            selectedCommunication={selectedCommunication}
            setSelectedCommunication={setSelectedCommunication}
          />
          
          {/* Right Panel - Tasks */}
          <TasksPanel 
            tasks={mockTasks} 
            stats={mockStats}
            selectedTask={selectedTask}
            setSelectedTask={handleTaskClick}
          />
        </div>
      </div>
      
      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Dashboard;