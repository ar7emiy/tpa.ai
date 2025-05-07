// Mock communications data 


// Communications data
export const mockCommunications = [
    {
      id: 1,
      type: "email",
      icon: "E",
      iconColor: "#0d6efd",
      from: "Robert Johnson (Claimant)",
      subject: "Medical treatment authorization request",
      preview: "I've attached the doctor's recommendation for physical therapy...",
      date: "Today at 9:43 AM",
      isNew: true,
      content: "Dear Mr. Smith,\n\nI've attached the doctor's recommendation for physical therapy for my lower back injury. Dr. Sarah Williams has recommended 3 sessions per week for 6 weeks at City Physical Therapy Center. Please let me know if you need any additional information to authorize this treatment.\n\nThank you,\nRobert Johnson",
      attachments: [
        { name: "DoctorRecommendation.pdf", size: "1.2 MB" }
      ]
    },
    {
      id: 2,
      type: "phone",
      icon: "P",
      iconColor: "#dc3545",
      from: "Dr. Sarah Williams",
      subject: "Workers comp claim #WC-2025-04872",
      preview: "Call summary: Discussion about claimant's work restrictions...",
      date: "Yesterday at 4:15 PM",
      isNew: true,
      content: "Dr. Williams called to discuss Robert Johnson's work restrictions. She stated that he should be limited to light duty with no lifting over 15 pounds for the next 4 weeks. She also recommended physical therapy sessions and provided details about her diagnosis (lumbar strain). Call duration: 8 minutes.",
      attachments: []
    },
    {
      id: 3,
      type: "fax",
      icon: "F",
      iconColor: "#6610f2",
      from: "Memorial Hospital",
      subject: "Updated medical records for Johnson, Robert",
      preview: "6 pages received including MRI results and specialist consult...",
      date: "04/28/2025 at 11:22 AM",
      isNew: false,
      content: "Fax received from Memorial Hospital containing updated medical records for Robert Johnson. Includes MRI results showing mild disc bulging at L4-L5 without nerve compression, diagnoses of lumbar sprain (S33.5XXA) and low back pain (M54.5), and specialist consultation notes recommending conservative treatment.",
      attachments: [
        { name: "JohnsonRobert_MRI.pdf", size: "3.5 MB" },
        { name: "JohnsonRobert_ConsultNotes.pdf", size: "1.8 MB" }
      ]
    },
    {
      id: 4,
      type: "email",
      icon: "E",
      iconColor: "#0d6efd",
      from: "Maria Garcia (HR Manager)",
      subject: "Return to Work Plan - Robert Johnson",
      preview: "We've prepared a modified duty plan based on doctor's recommendations...",
      date: "04/27/2025 at 3:37 PM",
      isNew: false,
      content: "Hello John,\n\nWe've prepared a modified duty plan for Robert Johnson based on the doctor's recommendations. He will be assigned to our shipping department for light-duty work that doesn't require lifting more than 15 pounds. His supervisor has been informed and will ensure compliance with all restrictions.\n\nPlease review the attached plan and let me know if you have any questions or suggestions.\n\nRegards,\nMaria Garcia\nHR Manager\nAcme Manufacturing Co.",
      attachments: [
        { name: "Johnson_RTW_Plan.docx", size: "542 KB" }
      ]
    },
    {
      id: 5,
      type: "note",
      icon: "N",
      iconColor: "#198754",
      from: "James Wilson (Adjuster)",
      subject: "Claim Reserve Adjustment",
      preview: "Increasing medical reserves based on specialist referral and possible surgery...",
      date: "04/26/2025 at 9:15 AM",
      isNew: false,
      content: "Adjusting claim reserves based on recent medical reports for Robert Johnson. Increasing medical reserves from $5,000 to $15,000 due to specialist referral and possible surgical intervention if conservative treatment fails. Indemnity reserves remain unchanged at this time. Will reassess after receiving additional information about treatment outcomes.",
      attachments: []
    }
  ];
  
  export default mockCommunications;