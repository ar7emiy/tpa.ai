import React from 'react';

const UserAvatar = ({ initials }) => {
  return (
    <div className="w-8 h-8 rounded-full bg-gray-200 border flex items-center justify-center">
      <span className="text-xs text-gray-800">{initials}</span>
    </div>
  );
};

export default UserAvatar;