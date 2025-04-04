# agents/verification_agent.py
import datetime
from typing import Dict, Any, Tuple
from .base_agent import BaseAgent
from google.generativeai.types import FunctionDeclaration, Tool

class VerificationAgent(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.0-pro"):
        super().__init__(model_name)
        self.system_prompt = self._format_system_prompt(
            "Verification Agent",
            """Your responsibilities:
            1. Verify employee status and eligibility
            2. Validate insurance policy details
            3. Confirm employment information
            4. Determine if the claim meets basic eligibility requirements
            
            Be thorough and fair in your verification process."""
        )
        
        # Define tools for this agent
        self.tools = [
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="verify_employment",
                        description="Verify employment status and eligibility",
                        parameters={
                            "type": "object",
                            "properties": {
                                "employment_verified": {"type": "boolean", "description": "Whether employment is verified"},
                                "verification_method": {"type": "string", "description": "Method used for verification"},
                                "employment_duration": {"type": "string", "description": "Duration of employment"},
                                "eligible_for_benefits": {"type": "boolean", "description": "Whether employee is eligible for benefits"},
                                "notes": {"type": "string", "description": "Any additional verification notes"}
                            },
                            "required": ["employment_verified", "eligible_for_benefits"]
                        }
                    ),
                    FunctionDeclaration(
                        name="verify_policy",
                        description="Verify insurance policy details",
                        parameters={
                            "type": "object",
                            "properties": {
                                "policy_number": {"type": "string", "description": "Insurance policy number"},
                                "policy_valid": {"type": "boolean", "description": "Whether policy is valid"},
                                "coverage_start_date": {"type": "string", "description": "Policy coverage start date"},
                                "coverage_end_date": {"type": "string", "description": "Policy coverage end date"},
                                "coverage_type": {"type": "string", "description": "Type of coverage provided"},
                                "adequate_coverage": {"type": "boolean", "description": "Whether coverage is adequate for claim"}
                            },
                            "required": ["policy_valid", "adequate_coverage"]
                        }
                    )
                ]
            )
        ]
        
        # Create the Gemini model
        self.model = self.create_gemini_model(self.system_prompt, self.tools)
    
    def handle_function_call(self, function_name: str, function_args: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Handle function calls from the model."""
        response = None
        updated_state = {}
        
        if function_name == "verify_employment":
            # Store employment verification in state
            updated_state["verification_status"] = {
                "employment": function_args,
                "verification_timestamp": datetime.datetime.now().isoformat()
            }
            response = "Employment verification complete"
            
        elif function_name == "verify_policy":
            # Store policy verification in state
            if "verification_status" not in updated_state:
                updated_state["verification_status"] = {}
            
            updated_state["verification_status"]["policy"] = function_args
            updated_state["verification_status"]["verification_timestamp"] = datetime.datetime.now().isoformat()
            response = "Policy verification complete"
            
        return response, updated_state
    
    def verify_employment(self, claim_id: str, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify employment status and eligibility."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the verification prompt
        prompt = f"""
        I need to verify employment status for claim {claim_id}.
        
        Employee data: {json.dumps(employee_data)}
        
        Please analyze this information and verify:
        1. Is the employment status confirmed?
        2. Is the employee eligible for workers' compensation benefits?
        
        Use the verify_employment function to record your findings.
        """
        
        # Generate the verification analysis
        response = chat.send_message(prompt)
        
        # Check for function calls
        verification_result = {}
        if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call"):
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = json.loads(function_call.args)
                    
                    if function_name == "verify_employment":
                        verification_result = function_args
        
        # Return the verification result
        return {
            "claim_id": claim_id,
            "verification_timestamp": datetime.datetime.now().isoformat(),
            "employment_verified": verification_result.get("employment_verified", False),
            "eligible_for_benefits": verification_result.get("eligible_for_benefits", False),
            "verification_method": verification_result.get("verification_method", "AI analysis"),
            "verification_notes": verification_result.get("notes", "")
        }
    
    def validate_policy(self, claim_id: str, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate insurance policy details."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the policy validation prompt
        prompt = f"""
        I need to validate insurance policy details for claim {claim_id}.
        
        Policy data: {json.dumps(policy_data)}
        
        Please analyze this information and verify:
        1. Is the policy valid?
        2. Does the policy provide adequate coverage for this claim?
        
        Use the verify_policy function to record your findings.
        """
        
        # Generate the policy validation analysis
        response = chat.send_message(prompt)
        
        # Check for function calls
        validation_result = {}
        if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call"):
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = json.loads(function_call.args)
                    
                    if function_name == "verify_policy":
                        validation_result = function_args
        
        # Return the policy validation result
        return {
            "claim_id": claim_id,
            "validation_timestamp": datetime.datetime.now().isoformat(),
            "policy_number": validation_result.get("policy_number", ""),
            "policy_valid": validation_result.get("policy_valid", False),
            "coverage_adequate": validation_result.get("adequate_coverage", False),
            "policy_validation_notes": validation_result.get("notes", "")
        }
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state."""
        claim_id = state.get("claim_id")
        status = state.get("status")
        
        if status == "verification":
            # Verify employment based on claimant and employer info
            claimant_info = state.get("claimant_info", {})
            employer_info = state.get("employer_info", {})
            
            # Combine data for verification
            employee_data = {
                **claimant_info,
                "employer": employer_info
            }
            
            # Perform employment verification
            verification_result = self.verify_employment(claim_id, employee_data)
            
            # Update state with verification results
            state["verification_status"] = verification_result
            state["current_agent"] = self.agent_name
            
            # Move to medical review if verification passes
            if verification_result.get("employment_verified") and verification_result.get("eligible_for_benefits"):
                state["status"] = "medical_review"
            else:
                # If verification fails, set to denied
                state["status"] = "denied"
                state["decision_status"] = {
                    "approved": False,
                    "decision_date": datetime.datetime.now().isoformat(),
                    "reasoning": "Failed employment verification: " + verification_result.get("verification_notes", "")
                }
        
        # Update timestamp
        state["updated_at"] = datetime.datetime.now().isoformat()
        
        return state
