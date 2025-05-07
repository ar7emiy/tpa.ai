// Consolidated mock data exports
import mockUser from './mockUser';
import mockCommunications from './mockCommunications';
import mockTasks from './mockTasks';
import mockClaimData from './mockClaimData';
import mockStats from './mockStats';

export { mockUser, mockCommunications, mockTasks, mockClaimData, mockStats };

// Additional mock collections for future use
export const mockProviders = [
  { id: 1, name: "Memorial Hospital", type: "Hospital", address: "123 Main St, New York, NY", phone: "212-555-1234" },
  { id: 2, name: "City Physical Therapy Center", type: "Therapy", address: "456 Park Ave, New York, NY", phone: "212-555-5678" },
  { id: 3, name: "Dr. Sarah Williams", type: "Specialist", address: "789 Broadway, New York, NY", phone: "212-555-9012" },
  { id: 4, name: "WorkMed Clinic", type: "Urgent Care", address: "321 Lexington Ave, New York, NY", phone: "212-555-3456" }
];

export const mockEmployers = [
  { id: 1, name: "Acme Manufacturing Co.", industry: "Manufacturing", address: "100 Industrial Way, New York, NY", contact: "Maria Garcia", phone: "212-555-7890" },
  { id: 2, name: "Tech Solutions Inc.", industry: "Technology", address: "200 Silicon St, New York, NY", contact: "David Chen", phone: "212-555-4567" },
  { id: 3, name: "Northeast Distribution", industry: "Logistics", address: "300 Commerce Blvd, New York, NY", contact: "James Wilson", phone: "212-555-8901" }
];

export const mockAdjusters = [
  { id: 1, name: "John Smith", email: "john.smith@claimspro.com", phone: "212-555-2345", activeClaims: 42 },
  { id: 2, name: "Sarah Johnson", email: "sarah.johnson@claimspro.com", phone: "212-555-6789", activeClaims: 38 },
  { id: 3, name: "Michael Brown", email: "michael.brown@claimspro.com", phone: "212-555-0123", activeClaims: 45 }
];