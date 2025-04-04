# agents/compliance_agent.py
import datetime
import json
from typing import Dict, List, Any, Tuple
from .base_agent import BaseAgent
from google.generativeai.types import FunctionDeclaration, Tool

class ComplianceAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.system_prompt = self._format_system_prompt(
            "Compliance Agent",
            """Your responsibilities:
            1. Ensure all required documentation is complete and accurate
            2. Verify timely reporting of incidents and claims
            3. Check that medical documentation meets regulatory requirements
            4. Ensure compliance with state-specific workers' compensation regulations
            5. Identify any compliance issues that could affect claim processing
            
            Be thorough and detail-oriented in your compliance assessments."""
        )
        
        # Define tools for this agent
        self.tools = [
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="verify_documentation",
                        description="Verify that all required documentation is present and complete",
                        parameters={
                            "type": "object",
                            "properties": {
                                "documentation_complete": {"type": "boolean", "description": "Whether all required documentation is complete"},
                                "missing_documents": {"type": "array", "items": {"type": "string"}, "description": "List of missing documents"},
                                "incomplete_documents": {"type": "array", "items": {"type": "string"}, "description": "List of incomplete documents"},
                                "documentation_quality": {"type": "string", "description": "Assessment of documentation quality (good, adequate, poor)"},
                                "notes": {"type": "string", "description": "Additional notes on documentation"}
                            },
                            "required": ["documentation_complete"]
                        }
                    ),
                    FunctionDeclaration(
                        name="check_reporting_timeline",
                        description="Check if incident and claim were reported within required timeframes",
                        parameters={
                            "type": "object",
                            "properties": {
                                "timely_reporting": {"type": "boolean", "description": "Whether reporting was timely"},
                                "incident_date": {"type": "string", "description": "Date of incident (ISO format)"},
                                "employer_notification_date": {"type": "string", "description": "Date employer was notified (ISO format)"},
                                "claim_filing_date": {"type": "string", "description": "Date claim was filed (ISO format)"},
                                "statutory_deadline": {"type": "string", "description": "Statutory deadline for filing (ISO format)"},
                                "within_deadline": {"type": "boolean", "description": "Whether claim was filed within statutory deadline"},
                                "delay_reason": {"type": "string", "description": "Reason for any delay in reporting or filing"}
                            },
                            "required": ["timely_reporting", "within_deadline"]
                        }
                    ),
                    FunctionDeclaration(
                        name="evaluate_compliance_status",
                        description="Evaluate overall compliance status of the claim",
                        parameters={
                            "type": "object",
                            "properties": {
                                "is_compliant": {"type": "boolean", "description": "Whether claim is compliant with requirements"},
                                "non_compliance_issues": {"type": "array", "items": {"type": "string"}, "description": "List of non-compliance issues"},
                                "needs_medical_info": {"type": "boolean", "description": "Whether additional medical information is needed"},
                                "needs_employment_info": {"type": "boolean", "description": "Whether additional employment information is needed"},
                                "regulatory_concerns": {"type": "array", "items": {"type": "string"}, "description": "Any regulatory concerns"},
                                "compliance_actions": {"type": "array", "items": {"type": "string"}, "description": "Actions needed to achieve compliance"}
                            },
                            "required": ["is_compliant"]
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
        
        if function_name == "verify_documentation":
            # Store documentation verification in state
            if "compliance_status" not in state:
                updated_state["compliance_status"] = {}
            
            updated_state["compliance_status"]["documentation"] = function_args
            updated_state["compliance_status"]["verification_timestamp"] = datetime.datetime.now().isoformat()
            response = "Documentation verification complete"
            
        elif function_name == "check_reporting_timeline":
            # Store timeline check in state
            if "compliance_status" not in state:
                updated_state["compliance_status"] = {}
            
            updated_state["compliance_status"]["timeline"] = function_args
            updated_state["compliance_status"]["verification_timestamp"] = datetime.datetime.now().isoformat()
            response = "Reporting timeline check complete"
            
        elif function_name == "evaluate_compliance_status":
            # Store overall compliance evaluation in state
            if "compliance_status" not in state:
                updated_state["compliance_status"] = {}
            
            updated_state["compliance_status"]["overall_status"] = function_args
            updated_state["compliance_status"]["is_compliant"] = function_args.get("is_compliant", False)
            updated_state["compliance_status"]["needs_medical_info"] = function_args.get("needs_medical_info", False)
            updated_state["compliance_status"]["verification_timestamp"] = datetime.datetime.now().isoformat()
            response = "Compliance evaluation complete"
        
        return response, updated_state
    
    def verify_documentation(self, claim_id: str, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify that all required documentation is present and complete."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the documentation verification prompt
        prompt = f"""
        I need to verify documentation for claim {claim_id}.
        
        Claim data: {json.dumps(claim_data)}
        
        Please verify:
        1. Is all required documentation present?
        2. Are there any missing or incomplete documents?
        3. What is the quality of the documentation provided?
        
        Required documents typically include:
        - First report of injury
        - Medical reports and diagnoses
        - Employer confirmation
        - Witness statements (if applicable)
        - Treatment plans
        - Work restriction documentation
        
        Use the verify_documentation function to record your findings.
        """
        
        try:
            # Generate the documentation verification
            response = chat.send_message(prompt)
            
            # Check for function calls
            verification_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "verify_documentation":
                            verification_result = function_args
            
            # Return the verification result
            return {
                "claim_id": claim_id,
                "verification_timestamp": datetime.datetime.now().isoformat(),
                **verification_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "verification_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "documentation_complete": False,
                "missing_documents": ["Unable to determine due to error"],
                "notes": f"Error verifying documentation: {str(e)}"
            }
    
    def check_reporting_timeline(self, claim_id: str, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if incident and claim were reported within required timeframes."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the timeline check prompt
        prompt = f"""
        I need to check the reporting timeline for claim {claim_id}.
        
        Claim data: {json.dumps(claim_data)}
        
        Please verify:
        1. When did the incident occur?
        2. When was the employer notified?
        3. When was the claim filed?
        4. Was the claim reported within statutory deadlines (typically 30-90 days depending on jurisdiction)?
        5. Is there any reason for delay in reporting?
        
        Use the check_reporting_timeline function to record your findings.
        """
        
        try:
            # Generate the timeline check
            response = chat.send_message(prompt)
            
            # Check for function calls
            timeline_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "check_reporting_timeline":
                            timeline_result = function_args
            
            # Return the timeline check result
            return {
                "claim_id": claim_id,
                "check_timestamp": datetime.datetime.now().isoformat(),
                **timeline_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "check_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "timely_reporting": False,
                "within_deadline": False,
                "delay_reason": f"Error checking timeline: {str(e)}"
            }
    
    def evaluate_compliance(self, claim_id: str, doc_verification: Dict[str, Any], timeline_check: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate overall compliance status of the claim."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the compliance evaluation prompt
        prompt = f"""
        I need to evaluate the overall compliance status for claim {claim_id}.
        
        Documentation verification: {json.dumps(doc_verification)}
        Timeline check: {json.dumps(timeline_check)}
        
        Please evaluate:
        1. Is the claim compliant with all requirements?
        2. What non-compliance issues exist, if any?
        3. Is additional medical or employment information needed?
        4. Are there any regulatory concerns?
        5. What actions are needed to achieve compliance?
        
        Use the evaluate_compliance_status function to record your evaluation.
        """
        
        try:
            # Generate the compliance evaluation
            response = chat.send_message(prompt)
            
            # Check for function calls
            evaluation_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "evaluate_compliance_status":
                            evaluation_result = function_args
            
            # Return the evaluation result
            return {
                "claim_id": claim_id,
                "evaluation_timestamp": datetime.datetime.now().isoformat(),
                **evaluation_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "evaluation_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "is_compliant": False,
                "non_compliance_issues": ["Unable to determine due to error"],
                "needs_medical_info": True,
                "needs_employment_info": True,
                "compliance_actions": [f"Resolve error in compliance evaluation: {str(e)}"]
            }
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state."""
        claim_id = state.get("claim_id")
        status = state.get("status")
        
        if status == "compliance_check":
            # Extract relevant claim data for compliance checks
            claim_data = {
                "claimant_info": state.get("claimant_info", {}),
                "employer_info": state.get("employer_info", {}),
                "injury_details": state.get("injury_details", {}),
                "medical_records": state.get("medical_records", []),
                "medical_assessment": state.get("medical_assessment", {}),
                "verification_status": state.get("verification_status", {})
            }
            
            # Verify documentation
            doc_verification = self.verify_documentation(claim_id, claim_data)
            if "compliance_status" not in state:
                state["compliance_status"] = {}
            state["compliance_status"]["documentation"] = doc_verification
            
            # Check reporting timeline
            timeline_check = self.check_reporting_timeline(claim_id, claim_data)
            state["compliance_status"]["timeline"] = timeline_check
            
            # Evaluate overall compliance
            compliance_evaluation = self.evaluate_compliance(claim_id, doc_verification, timeline_check)
            state["compliance_status"]["overall_status"] = compliance_evaluation
            state["compliance_status"]["is_compliant"] = compliance_evaluation.get("is_compliant", False)
            state["compliance_status"]["needs_medical_info"] = compliance_evaluation.get("needs_medical_info", False)
            state["current_agent"] = self.agent_name
            
            # Update status based on compliance
            if compliance_evaluation.get("is_compliant", False):
                state["status"] = "decision_pending"
            elif compliance_evaluation.get("needs_medical_info", False):
                state["status"] = "medical_review"
            else:
                state["status"] = "verification"
        
        # Update timestamp
        state["updated_at"] = datetime.datetime.now().isoformat()
        
        return state
