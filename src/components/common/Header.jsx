import React from 'react';
import { useNavigate } from 'react-router-dom';
import UserAvatar from './UserAvatar';

const Header = ({ user, activeTab, setActiveTab }) => {
  const navigate = useNavigate();
  const tabs = ["Dashboard", "Claims", "Reports", "Settings"];
  
  const handleTabClick = (tab) => {
    setActiveTab(tab);
    
    // Navigate based on the tab clicked
    switch(tab) {
      case "Dashboard":
        navigate('/dashboard');
        break;
      case "Claims":
        // This would typically go to a claims listing page
        // For now, we'll keep the user on the current page if they're in a claim
        if (!window.location.pathname.includes('/claims/')) {
          navigate('/dashboard');
        }
        break;
      case "Reports":
        navigate('/reports');
        break;
      case "Settings":
        navigate('/settings');
        break;
      default:
        navigate('/dashboard');
    }
  };
  
  return (
    <header className="bg-blue-700 text-white">
      <div className="flex items-center h-12">
        <div className="font-bold text-lg px-4">ClaimsPro AI</div>
        
        {/* Navigation Tabs */}
        <div className="flex">
          {tabs.map(tab => (
            <div 
              key={tab}
              className={`w-24 h-12 flex items-center justify-center cursor-pointer ${activeTab === tab ? 'bg-blue-600' : 'bg-blue-700'}`}
              onClick={() => handleTabClick(tab)}
            >
              <span className="text-sm">{tab}</span>
            </div>
          ))}
        </div>
        
        {/* User Info */}
        <div className="ml-auto flex items-center pr-4">
          <span className="text-sm mr-2">{user.name}</span>
          <UserAvatar initials={user.initials} />
        </div>
      </div>
    </header>
  );
};

export default Header;