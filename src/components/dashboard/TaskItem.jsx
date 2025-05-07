// TaskItem component 

import React from 'react';

const TaskItem = ({ task, isSelected, onClick }) => {
  return (
    <div 
      className={`border border-t-0 px-2 py-3 flex ${
        task.highlighted ? 'bg-blue-50 border-blue-400 border-2' : 'bg-white'
      } ${isSelected ? 'ring-2 ring-blue-500' : ''}`}
      onClick={onClick}
    >
      <div className="w-16">
        <div 
          className="px-2 py-0.5 rounded-full text-white text-xs text-center"
          style={{ backgroundColor: task.priorityColor }}
        >
          {task.priority}
        </div>
      </div>
      
      <div className="w-28 text-xs">{task.claimNumber}</div>
      
      <div className="flex-1">
        <div className="text-xs font-bold">{task.title}</div>
        <div className="text-xs text-gray-500 mt-0.5">{task.description}</div>
        {task.relatedComms > 0 && (
          <div className="text-xs text-blue-600 mt-0.5">
            Related to {task.relatedComms} communication{task.relatedComms > 1 ? 's' : ''}
          </div>
        )}
      </div>
      
      <div className="w-24 text-xs">
        <span className={task.isDueToday ? 'text-red-500 font-bold' : ''}>
          {task.dueDate}
        </span>
      </div>
      
      <div className="w-24 text-xs">{task.assignedTo}</div>
    </div>
  );
};

export default TaskItem;