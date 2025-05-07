// StatsCard component 

import React from 'react';

const StatsCard = ({ count, label, colorClass, borderClass }) => {
  return (
    <div className={`flex-1 ${colorClass} ${borderClass} p-2 rounded text-center`}>
      <div className={`text-xl font-bold ${borderClass.replace('border-', 'text-')}`}>{count}</div>
      <div className="text-xs">{label}</div>
    </div>
  );
};

export default StatsCard;