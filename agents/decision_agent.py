# agents/decision_agent.py
import datetime
import json
from typing import Dict, List, Any, Tuple
from .base_agent import BaseAgent
from google.generativeai.types import FunctionDeclaration, Tool

class DecisionAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.system_prompt = self._format_system_prompt(
            "Decision Agent",
            """Your responsibilities:
            1. Evaluate all evidence and information collected about the claim
            2. Determine if the injury is work-related
            3. Assess compensability based on applicable laws
            4. Make a fair and objective decision to approve or deny the claim
            5. Calculate appropriate compensation if approved
            6. Document reasoning behind decisions
            
            Be balanced and fair in your evaluation, considering both the claimant's and employer's perspectives."""
        )
        
        # Define tools for this agent
        self.tools = [
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="evaluate_evidence",
                        description="Evaluate evidence collected for the claim",
                        parameters={
                            "type": "object",
                            "properties": {
                                "evidence_sufficient": {"type": "boolean", "description": "Whether evidence is sufficient for decision"},
                                "work_relatedness": {"type": "string", "description": "Assessment of work-relatedness (confirmed, likely, unlikely, unrelated)"},
                                "key_supporting_factors": {"type": "array", "items": {"type": "string"}, "description": "Key factors supporting the claim"},
                                "key_contradicting_factors": {"type": "array", "items": {"type": "string"}, "description": "Key factors contradicting the claim"},
                                "credibility_issues": {"type": "array", "items": {"type": "string"}, "description": "Any credibility issues identified"},
                                "evidence_gaps": {"type": "array", "items": {"type": "string"}, "description": "Gaps in evidence"}
                            },
                            "required": ["evidence_sufficient", "work_relatedness"]
                        }
                    ),
                    FunctionDeclaration(
                        name="determine_compensability",
                        description="Determine if claim is compensable under workers' compensation laws",
                        parameters={
                            "type": "object",
                            "properties": {
                                "compensable": {"type": "boolean", "description": "Whether the claim is compensable"},
                                "compensability_factors": {"type": "array", "items": {"type": "string"}, "description": "Factors affecting compensability"},
                                "legal_basis": {"type": "string", "description": "Legal basis for determination"},
                                "jurisdictional_requirements_met": {"type": "boolean", "description": "Whether jurisdictional requirements are met"},
                                "statutory_exclusions": {"type": "array", "items": {"type": "string"}, "description": "Any applicable statutory exclusions"}
                            },
                            "required": ["compensable"]
                        }
                    ),
                    FunctionDeclaration(
                        name="make_claim_decision",
                        description="Make final decision on the claim",
                        parameters={
                            "type": "object",
                            "properties": {
                                "approved": {"type": "boolean", "description": "Whether claim is approved"},
                                "decision_date": {"type": "string", "description": "Date of decision (ISO format)"},
                                "effective_date": {"type": "string", "description": "Effective date of decision (ISO format)"},
                                "reasoning": {"type": "string", "description": "Detailed reasoning for decision"},
                                "benefit_type": {"type": "string", "description": "Type of benefits approved (if applicable)"},
                                "denial_reason": {"type": "string", "description": "Reason for denial (if applicable)"},
                                "appeal_rights": {"type": "string", "description": "Information on appeal rights"}
                            },
                            "required": ["approved", "decision_date", "reasoning"]
                        }
                    ),
                    FunctionDeclaration(
                        name="calculate_compensation",
                        description="Calculate compensation amount for approved claim",
                        parameters={
                            "type": "object",
                            "properties": {
                                "compensation_type": {"type": "string", "description": "Type of compensation (temporary total, temporary partial, permanent partial, etc.)"},
                                "weekly_amount": {"type": "number", "description": "Weekly compensation amount"},
                                "calculation_basis": {"type": "string", "description": "Basis for calculation (e.g., average weekly wage)"},
                                "estimated_duration": {"type": "string", "description": "Estimated duration of payments"},
                                "maximum_benefit": {"type": "number", "description": "Maximum benefit amount"},
                                "waiting_period": {"type": "string", "description": "Applicable waiting period"},
                                "retroactive_amount": {"type": "number", "description": "Any retroactive payment due"}
                            },
                            "required": ["compensation_type", "weekly_amount"]
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
        
        if function_name == "evaluate_evidence":
            # Store evidence evaluation in state
            if "decision_status" not in state:
                updated_state["decision_status"] = {}
            
            updated_state["decision_status"]["evidence_evaluation"] = function_args
            updated_state["decision_status"]["evaluation_timestamp"] = datetime.datetime.now().isoformat()
            response = "Evidence evaluation complete"
            
        elif function_name == "determine_compensability":
            # Store compensability determination in state
            if "decision_status" not in state:
                updated_state["decision_status"] = {}
            
            updated_state["decision_status"]["compensability"] = function_args
            updated_state["decision_status"]["evaluation_timestamp"] = datetime.datetime.now().isoformat()
            response = "Compensability determination complete"
            
        elif function_name == "make_claim_decision":
            # Store claim decision in state
            if "decision_status" not in state:
                updated_state["decision_status"] = {}
            
            updated_state["decision_status"]["decision"] = function_args
            updated_state["decision_status"]["approved"] = function_args.get("approved", False)
            updated_state["decision_status"]["decision_date"] = function_args.get("decision_date", datetime.datetime.now().isoformat())
            updated_state["decision_status"]["reasoning"] = function_args.get("reasoning", "")
            response = "Claim decision complete"
            
        elif function_name == "calculate_compensation":
            # Store compensation calculation in state
            if "decision_status" not in state:
                updated_state["decision_status"] = {}
            
            updated_state["decision_status"]["compensation"] = function_args
            updated_state["decision_status"]["weekly_amount"] = function_args.get("weekly_amount", 0)
            response = "Compensation calculation complete"
        
        return response, updated_state
    
    def evaluate_evidence(self, claim_id: str, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate evidence collected for the claim."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the evidence evaluation prompt
        prompt = f"""
        I need to evaluate the evidence for claim {claim_id}.
        
        Claim data: {json.dumps(claim_data)}
        
        Please evaluate:
        1. Is the evidence sufficient to make a decision?
        2. Is the injury/illness work-related based on the evidence?
        3. What key factors support or contradict the claim?
        4. Are there any credibility issues with the evidence?
        5. Are there any significant gaps in the evidence?
        
        Use the evaluate_evidence function to record your evaluation.
        """
        
        try:
            # Generate the evidence evaluation
            response = chat.send_message(prompt)
            
            # Check for function calls
            evaluation_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "evaluate_evidence":
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
                "evidence_sufficient": False,
                "work_relatedness": "unknown",
                "evidence_gaps": [f"Error evaluating evidence: {str(e)}"]
            }
    
    def determine_compensability(self, claim_id: str, evidence_evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Determine if claim is compensable under workers' compensation laws."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the compensability determination prompt
        prompt = f"""
        I need to determine compensability for claim {claim_id} based on the evidence evaluation.
        
        Evidence evaluation: {json.dumps(evidence_evaluation)}
        
        Please determine:
        1. Is the claim compensable under typical workers' compensation laws?
        2. What factors affect compensability in this case?
        3. Are all jurisdictional requirements met?
        4. Are there any statutory exclusions that would apply?
        
        Use the determine_compensability function to record your determination.
        """
        
        try:
            # Generate the compensability determination
            response = chat.send_message(prompt)
            
            # Check for function calls
            determination_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "determine_compensability":
                            determination_result = function_args
            
            # Return the determination result
            return {
                "claim_id": claim_id,
                "determination_timestamp": datetime.datetime.now().isoformat(),
                **determination_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "determination_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "compensable": False,
                "compensability_factors": [f"Error determining compensability: {str(e)}"]
            }
    
    def make_claim_decision(self, claim_id: str, evidence_evaluation: Dict[str, Any], compensability: Dict[str, Any]) -> Dict[str, Any]:
        """Make final decision on the claim."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the claim decision prompt
        prompt = f"""
        I need to make a final decision on claim {claim_id} based on the evidence evaluation and compensability determination.
        
        Evidence evaluation: {json.dumps(evidence_evaluation)}
        Compensability determination: {json.dumps(compensability)}
        
        Please make a decision:
        1. Should the claim be approved or denied?
        2. What is the detailed reasoning for this decision?
        3. What type of benefits should be approved (if applicable)?
        4. What is the specific reason for denial (if applicable)?
        5. What appeal rights should be communicated?
        
        Use the make_claim_decision function to record your decision.
        """
        
        try:
            # Generate the claim decision
            response = chat.send_message(prompt)
            
            # Check for function calls
            decision_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "make_claim_decision":
                            decision_result = function_args
            
            # If decision_date not provided, use current date
            if "decision_date" not in decision_result:
                decision_result["decision_date"] = datetime.datetime.now().isoformat()
            
            # Return the decision result
            return {
                "claim_id": claim_id,
                **decision_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "approved": False,
                "decision_date": datetime.datetime.now().isoformat(),
                "reasoning": f"Error making claim decision: {str(e)}",
                "denial_reason": f"Technical error: {str(e)}",
                "appeal_rights": "Claimant has the right to appeal this decision."
            }
    
    def calculate_compensation(self, claim_id: str, claim_data: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate compensation amount for approved claim."""
        # Only calculate if claim is approved
        if not decision.get("approved", False):
            return {
                "claim_id": claim_id,
                "calculation_timestamp": datetime.datetime.now().isoformat(),
                "compensation_type": "none",
                "weekly_amount": 0,
                "calculation_basis": "Claim denied - no compensation",
                "estimated_duration": "0",
                "notes": "No compensation due - claim denied"
            }
        
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the compensation calculation prompt
        prompt = f"""
        I need to calculate compensation for approved claim {claim_id}.
        
        Claim data: {json.dumps(claim_data)}
        Decision: {json.dumps(decision)}
        
        Please calculate:
        1. What type of compensation is appropriate?
        2. What should the weekly compensation amount be?
        3. What is the basis for this calculation?
        4. What is the estimated duration of payments?
        5. Is there any retroactive payment due?
        
        For this simulation, you can assume:
        - Temporary total disability (TTD) is typically 2/3 of the average weekly wage
        - Temporary partial disability (TPD) is typically calculated based on wage loss
        - Permanent partial disability (PPD) depends on impairment rating
        
        Use the calculate_compensation function to record your calculation.
        """
        
        try:
            # Generate the compensation calculation
            response = chat.send_message(prompt)
            
            # Check for function calls
            calculation_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "calculate_compensation":
                            calculation_result = function_args
            
            # Return the calculation result
            return {
                "claim_id": claim_id,
                "calculation_timestamp": datetime.datetime.now().isoformat(),
                **calculation_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "calculation_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "compensation_type": "unknown",
                "weekly_amount": 0,
                "calculation_basis": f"Error calculating compensation: {str(e)}"
            }
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state."""
        claim_id = state.get("claim_id")
        status = state.get("status")
        
        if status == "decision_pending":
            # Extract relevant claim data for decision making
            claim_data = {
                "claimant_info": state.get("claimant_info", {}),
                "employer_info": state.get("employer_info", {}),
                "injury_details": state.get("injury_details", {}),
                "medical_records": state.get("medical_records", []),
                "medical_assessment": state.get("medical_assessment", {}),
                "verification_status": state.get("verification_status", {}),
                "compliance_status": state.get("compliance_status", {}),
                "work_restrictions": state.get("work_restrictions", {})
            }
            
            # Evaluate evidence
            evidence_evaluation = self.evaluate_evidence(claim_id, claim_data)
            if "decision_status" not in state:
                state["decision_status"] = {}
            state["decision_status"]["evidence_evaluation"] = evidence_evaluation
            
            # Determine compensability
            compensability = self.determine_compensability(claim_id, evidence_evaluation)
            state["decision_status"]["compensability"] = compensability
            
            # Make claim decision
            decision = self.make_claim_decision(claim_id, evidence_evaluation, compensability)
            state["decision_status"]["decision"] = decision
            state["decision_status"]["approved"] = decision.get("approved", False)
            state["decision_status"]["decision_date"] = decision.get("decision_date", datetime.datetime.now().isoformat())
            state["decision_status"]["reasoning"] = decision.get("reasoning", "")
            
            # Calculate compensation if approved
            if decision.get("approved", False):
                compensation = self.calculate_compensation(claim_id, claim_data, decision)
                state["decision_status"]["compensation"] = compensation
                state["decision_status"]["weekly_amount"] = compensation.get("weekly_amount", 0)
                
                # Update status to approved
                state["status"] = "approved"
            else:
                # Update status to denied
                state["status"] = "denied"
            
            state["current_agent"] = self.agent_name
        
        # Update timestamp
        state["updated_at"] = datetime.datetime.now().isoformat()
        
        return state
