// Mock tasks data 

// Tasks data
export const mockTasks = [
    {
      id: 1,
      priority: "Critical",
      priorityColor: "#dc3545",
      claimNumber: "WC-2025-04872",
      title: "Medical Treatment Authorization",
      description: "Review PT prescription and authorize treatment",
      relatedComms: 2,
      dueDate: "Today",
      isDueToday: true,
      assignedTo: "John Smith",
      highlighted: true,
      claimant: "Robert Johnson",
      status: "Pending"
    },
    {
      id: 2,
      priority: "Critical",
      priorityColor: "#dc3545",
      claimNumber: "WC-2025-03541",
      title: "Update Reserves",
      description: "Adjust reserves based on surgical consultation",
      relatedComms: 1,
      dueDate: "Today",
      isDueToday: true,
      assignedTo: "John Smith",
      highlighted: false,
      claimant: "Michael Davis",
      status: "Pending"
    },
    {
      id: 3,
      priority: "High",
      priorityColor: "#ffc107",
      claimNumber: "WC-2025-04872",
      title: "Return to Work Plan",
      description: "Review modified duty plan from employer",
      relatedComms: 1,
      dueDate: "May 2, 2025",
      isDueToday: false,
      assignedTo: "John Smith",
      highlighted: false,
      claimant: "Robert Johnson",
      status: "Pending"
    },
    {
      id: 4,
      priority: "High",
      priorityColor: "#ffc107",
      claimNumber: "WC-2025-03892",
      title: "Update Medical Status",
      description: "Document recent doctor visit and update disability status",
      relatedComms: 0,
      dueDate: "May 3, 2025",
      isDueToday: false,
      assignedTo: "John Smith",
      highlighted: false,
      claimant: "Emma Wilson",
      status: "Pending"
    },
    {
      id: 5,
      priority: "High",
      priorityColor: "#ffc107",
      claimNumber: "WC-2025-04103",
      title: "Compensability Determination",
      description: "Make final determination on claim compensability",
      relatedComms: 0,
      dueDate: "May 5, 2025",
      isDueToday: false,
      assignedTo: "Sarah Johnson",
      highlighted: false,
      claimant: "David Thompson",
      status: "Pending"
    }
  ];
  
  export default mockTasks;