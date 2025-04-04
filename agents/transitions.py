# workflow/transitions.py
from typing import Dict, Any, Callable, Tuple
from .states import ClaimStatus

class WorkflowTransitionManager:
    def __init__(self):
        """Initialize the transition manager with standard transitions."""
        self.transitions = self._initialize_transitions()
    
    def _initialize_transitions(self):
        """Initialize standard transitions based on the workflow diagram."""
        transitions = {
            # From New to Verification
            ClaimStatus.NEW: lambda state: (
                ClaimStatus.VERIFICATION,
                state
            ),
            
            # From Verification to Medical Review or Denied
            ClaimStatus.VERIFICATION: lambda state: (
                ClaimStatus.MEDICAL_REVIEW if state.get("verification_status", {}).get("employment_verified") and 
                                             state.get("verification_status", {}).get("eligible_for_benefits") 
                else ClaimStatus.DENIED,
                state
            ),
            
            # From Medical Review to Compliance Check
            ClaimStatus.MEDICAL_REVIEW: lambda state: (
                ClaimStatus.COMPLIANCE_CHECK if state.get("medical_records") 
                else ClaimStatus.MEDICAL_REVIEW,
                state
            ),
            
            # From Compliance Check to Decision Pending or back to previous steps
            ClaimStatus.COMPLIANCE_CHECK: lambda state: (
                ClaimStatus.DECISION_PENDING if state.get("compliance_status", {}).get("is_compliant") 
                else (ClaimStatus.MEDICAL_REVIEW if state.get("compliance_status", {}).get("needs_medical_info") 
                      else ClaimStatus.VERIFICATION),
                state
            ),
            
            # From Decision Pending to Approved or Denied
            ClaimStatus.DECISION_PENDING: lambda state: (
                ClaimStatus.APPROVED if state.get("decision_status", {}).get("approved") 
                else ClaimStatus.DENIED,
                state
            ),
            
            # From Approved to Payment Processing
            ClaimStatus.APPROVED: lambda state: (
                ClaimStatus.PAYMENT_PROCESSING,
                state
            ),
            
            # From Payment Processing to Recovery Check
            ClaimStatus.PAYMENT_PROCESSING: lambda state: (
                ClaimStatus.RECOVERY_CHECK if state.get("payment_status", {}).get("payment_processed") 
                else ClaimStatus.PAYMENT_PROCESSING,
                state
            ),
            
            # From Recovery Check to Closed or back to Payment Processing
            ClaimStatus.RECOVERY_CHECK: lambda state: (
                ClaimStatus.CLOSED if state.get("recovery_status", {}).get("fully_recovered") 
                else ClaimStatus.PAYMENT_PROCESSING,
                state
            ),
            
            # Denied claims go to Closed
            ClaimStatus.DENIED: lambda state: (
                ClaimStatus.CLOSED,
                state
            )
        }
        
        return transitions
    
    def get_next_state(self, current_status: ClaimStatus, state: Dict[str, Any]) -> Tuple[ClaimStatus, Dict[str, Any]]:
        """Get the next state based on current status and state data."""
        if current_status in self.transitions:
            return self.transitions[current_status](state)
        
        # If no transition found, stay in same state
        return current_status, state
