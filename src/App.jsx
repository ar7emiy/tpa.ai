// Main App component 

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ClaimsProcessing from './pages/ClaimsProcessing';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

// Main App Component
const App = () => {
  return (
    <Router basename="/">
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/claims/:id" element={<ClaimsProcessing />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
};

export default App;