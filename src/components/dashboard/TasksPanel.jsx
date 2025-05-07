// TasksPanel component 

import React from 'react';
import TaskItem from './TaskItem';
import StatsCard from './StatsCard';

// Add a comment explaining that setSelectedTask now expects a taskId parameter
const TasksPanel = ({ tasks, stats, selectedTask, setSelectedTask }) => {
  const handleTaskSelect = (taskId) => {
    // Pass the taskId to the parent component's handler
    setSelectedTask(taskId);
  };

  return (
    <div className="w-1/2">
      {/* Panel Header */}
      <div className="bg-gray-200 h-12 flex items-center justify-between px-4">
        <h2 className="font-bold text-gray-800">Priority Tasks</h2>
        
        <div className="flex">
          <select className="px-2 py-1 text-xs border rounded mr-2 w-36">
            <option>Filter: All Tasks</option>
          </select>
          
          <button className="bg-blue-600 text-white px-4 py-1 text-xs rounded">
            + New Task
          </button>
        </div>
      </div>
      
      {/* Stats Cards */}
      <div className="flex px-4 pt-4 gap-4">
        <StatsCard 
          count={stats.critical} 
          label="Critical" 
          colorClass="bg-red-100" 
          borderClass="border-red-500" 
        />
        <StatsCard 
          count={stats.high} 
          label="High" 
          colorClass="bg-yellow-100" 
          borderClass="border-yellow-400" 
        />
        <StatsCard 
          count={stats.normal} 
          label="Normal" 
          colorClass="bg-green-100" 
          borderClass="border-green-500" 
        />
        <StatsCard 
          count={stats.completed} 
          label="Completed" 
          colorClass="bg-gray-200" 
          borderClass="border-gray-500" 
        />
      </div>
      
      {/* Tasks Table */}
      <div className="px-4 mt-4">
        {/* Table Header */}
        <div className="bg-gray-200 border px-2 py-2 flex text-xs font-bold">
          <div className="w-16">Priority</div>
          <div className="w-28">Claim #</div>
          <div className="flex-1">Task</div>
          <div className="w-24">Due Date</div>
          <div className="w-24">Assigned To</div>
        </div>
        
        {/* Table Body */}
        <div className="overflow-y-auto max-h-64">
          {tasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              isSelected={selectedTask === task.id}
              onClick={() => handleTaskSelect(task.id)}
            />
          ))}
        </div>
      </div>
      
      {/* Tab Interaction Hint */}
      <div className="mx-4 mt-4 bg-yellow-100 border border-yellow-400 rounded p-2 text-xs text-center">
        Press TAB on the highlighted task to enter detailed processing view
      </div>
      
      {/* Productivity Metrics */}
      <div className="mx-4 mt-4 bg-gray-100 border p-4">
        <div className="font-bold text-sm mb-2">Your Productivity</div>
        
        <div className="mb-2">
          <div className="bg-gray-200 rounded-full h-5 overflow-hidden">
            <div 
              className="bg-blue-600 h-5 rounded-full flex items-center pl-2 text-xs text-white"
              style={{ width: '75%' }}
            >
              Tasks Completed: 75%
            </div>
          </div>
        </div>
        
        <div>
          <div className="bg-gray-200 rounded-full h-5 overflow-hidden">
            <div 
              className="bg-green-500 h-5 rounded-full flex items-center pl-2 text-xs text-white"
              style={{ width: '80%' }}
            >
              Response Time: 80%
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TasksPanel;