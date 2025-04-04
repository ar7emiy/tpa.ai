# workflow/states.py
from typing import TypedDict, List, Dict, Any, Literal

class ClaimStatus(str, Enum):
    NEW = "new"
    VERIFICATION = "verification"
    MEDICAL_REVIEW = "medical_review"
    COMPLIANCE_CHECK = "compliance_check"
    DECISION_PENDING = "decision_pending"
    APPROVED = "approved"
    DENIED = "denied"
    PAYMENT_PROCESSING = "payment_processing"
    RECOVERY_CHECK = "recovery_check"
    ESCALATED = "escalated"
    CLOSED = "closed"

class ClaimState(TypedDict):
    # Identification
    claim_id: str
    status: ClaimStatus
    
    # Stakeholder Information
    claimant_info: Dict[str, Any]      # Personal details, contact info
    employer_info: Dict[str, Any]      # Company details, supervisor info
    
    # Claim Details
    injury_details: Dict[str, Any]     # Date, location, type, cause
    witness_info: List[Dict[str, Any]] # Names, contact info
    
    # Medical Information
    medical_records: List[Dict[str, Any]]  # Provider notes, diagnoses
    treatment_plan: Dict[str, Any]     # Recommended treatment
    work_restrictions: Dict[str, Any]  # Limitations, duration
    
    # Process Tracking
    verification_status: Dict[str, Any]  # Employment verified, eligibility
    compliance_status: Dict[str, Any]    # Documentation complete, timely filing
    decision_status: Dict[str, Any]      # Approved/denied, reasoning
    payment_status: Dict[str, Any]       # Amount, schedule
    recovery_status: Dict[str, Any]      # Recovery progress
    
    # Communication History
    conversations: Dict[str, List[Dict[str, Any]]]  # By stakeholder type
    
    # Metadata
    created_at: str
    updated_at: str
    current_agent: str  # Which agent is currently processing
