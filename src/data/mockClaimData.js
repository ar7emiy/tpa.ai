// Mock claim data 


// Claim data for the specific claim being processed
export const mockClaimData = {
    claimNumber: "WC-2025-04872",
    claimant: "Robert Johnson",
    injury: "Lower Back Injury",
    injuryDate: "04/15/2025",
    employer: "Acme Manufacturing Co.",
    adjuster: "John Smith",
    status: "Active",
    state: "New York",
    hasDueTask: true,
    dueTaskName: "Medical Authorization",
    
    // Treatment auth data
    treatment: {
      type: "Physical Therapy",
      provider: "City Physical Therapy Center",
      startDate: "05/05/2025",
      endDate: "06/15/2025",
      frequency: "3x per week",
      sessions: "18",
      primaryDiagnosis: "S33.5XXA - Lumbar Sprain",
      secondaryDiagnosis: "M54.5 - Low back pain",
      decision: "Approved",
      authCode: "AUTH-PT-458721",
      notes: "Authorization for 18 sessions of physical therapy, consistent with ODG guidelines for lumbar strain. Request progress reports after 9 sessions."
    },
    
    // Notes and sources
    notes: [
      {
        id: 1,
        title: "Medical Treatment Request",
        source: "Email from Dr. Sarah Williams (04/28/2025)",
        content: "\"Patient requires physical therapy 3x weekly for 6 weeks to address lumbar strain. Recommended provider: City Physical Therapy Center.\""
      },
      {
        id: 2,
        title: "Diagnostic Report",
        source: "Fax from Memorial Hospital (04/26/2025)",
        content: "\"MRI shows mild disc bulging at L4-L5 without nerve compression. Diagnosis: Lumbar sprain (S33.5XXA) with associated low back pain (M54.5). Conservative treatment recommended with physical therapy and anti-inflammatory medication.\""
      },
      {
        id: 3,
        title: "Prior Medical History",
        source: "Claim Notes (04/20/2025)",
        content: "\"Claimant reports no prior back injuries. Initial medical assessment indicates acute injury consistent with reported workplace incident.\""
      }
    ],
    
    aiRecommendation: {
      title: "AI Recommendation:",
      content: "Treatment request is consistent with ODG guidelines for diagnosis. Recommend approval."
    },
    
    // Additional claim information
    claimDetails: {
      dateOfHire: "06/15/2022",
      occupation: "Warehouse Associate",
      weeklyWage: "$950.00",
      injuryType: "Traumatic - Lifting",
      bodyParts: ["Lumbar Spine"],
      witnesses: ["James Peterson", "Anna Reynolds"],
      incidentDescription: "Employee was lifting a box of inventory from floor level to waist height when he felt a sharp pain in lower back. Immediate supervisor was notified within 15 minutes.",
      treatmentHistory: [
        {
          date: "04/15/2025",
          provider: "WorkMed Clinic",
          type: "Initial Assessment",
          notes: "Acute lumbar strain diagnosed. Prescribed muscle relaxants and anti-inflammatory medication."
        },
        {
          date: "04/22/2025",
          provider: "Memorial Hospital",
          type: "MRI Scan",
          notes: "Mild disc bulging L4-L5. No herniation or nerve compression detected."
        },
        {
          date: "04/25/2025",
          provider: "Dr. Sarah Williams - Orthopedics",
          type: "Specialist Consultation",
          notes: "Confirmed lumbar strain diagnosis. Recommended physical therapy and continued medication."
        }
      ]
    }
  };
  
  export default mockClaimData;