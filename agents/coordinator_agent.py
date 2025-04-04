# agents/coordinator_agent.py
import datetime
import json
from typing import Dict, List, Any, Tuple
from .base_agent import BaseAgent
from google.generativeai.types import FunctionDeclaration, Tool

class CoordinatorAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.system_prompt = self._format_system_prompt(
            "Coordinator Agent",
            """Your responsibilities:
            1. Orchestrate the overall workers' compensation claims process
            2. Determine the next appropriate step in the workflow
            3. Identify and handle special cases or exceptions
            4. Ensure all required information is gathered at each stage
            5. Monitor and report on claim progress
            6. Detect and address bottlenecks or delays
            
            Act as the central coordinator, guiding each claim through the appropriate workflow path."""
        )
        
        # Define tools for this agent
        self.tools = [
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="evaluate_claim_status",
                        description="Evaluate current status and determine next steps",
                        parameters={
                            "type": "object",
                            "properties": {
                                "current_status": {"type": "string", "description": "Current claim status"},
                                "recommended_next_status": {"type": "string", "description": "Recommended next status"},
                                "required_actions": {"type": "array", "items": {"type": "string"}, "description": "Actions required to move forward"},
                                "missing_information": {"type": "array", "items": {"type": "string"}, "description": "Missing information needed"},
                                "priority": {"type": "string", "description": "Claim priority (normal, high, urgent)"},
                                "escalation_needed": {"type": "boolean", "description": "Whether escalation is needed"},
                                "notes": {"type": "string", "description": "Additional coordination notes"}
                            },
                            "required": ["current_status", "recommended_next_status"]
                        }
                    ),
                    FunctionDeclaration(
                        name="identify_special_case",
                        description="Identify if claim requires special handling",
                        parameters={
                            "type": "object",
                            "properties": {
                                "is_special_case": {"type": "boolean", "description": "Whether claim requires special handling"},
                                "case_type": {"type": "string", "description": "Type of special case (complex, disputed, high-value, etc.)"},
                                "handling_instructions": {"type": "string", "description": "Special handling instructions"},
                                "additional_resources_needed": {"type": "array", "items": {"type": "string"}, "description": "Additional resources needed"},
                                "estimated_resolution_time": {"type": "string", "description": "Estimated time to resolution"}
                            },
                            "required": ["is_special_case"]
                        }
                    ),
                    FunctionDeclaration(
                        name="generate_status_update",
                        description="Generate a status update for the claim",
                        parameters={
                            "type": "object",
                            "properties": {
                                "status_summary": {"type": "string", "description": "Summary of current status"},
                                "progress_percentage": {"type": "number", "description": "Estimated percentage of completion"},
                                "last_activity": {"type": "string", "description": "Description of last activity"},
                                "next_steps": {"type": "array", "items": {"type": "string"}, "description": "Next steps in process"},
                                "blockers": {"type": "array", "items": {"type": "string"}, "description": "Current blockers or issues"},
                                "estimated_completion": {"type": "string", "description": "Estimated completion date (ISO format)"}
                            },
                            "required": ["status_summary", "progress_percentage", "next_steps"]
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
        
        if function_name == "evaluate_claim_status":
            # Update coordination status in state
            if "coordination_status" not in state:
                updated_state["coordination_status"] = {}
            
            updated_state["coordination_status"]["status_evaluation"] = function_args
            updated_state["coordination_status"]["evaluation_timestamp"] = datetime.datetime.now().isoformat()
            
            # If recommended next status is different, update it
            if function_args.get("recommended_next_status") != state.get("status"):
                updated_state["status"] = function_args.get("recommended_next_status")
            
            response = "Claim status evaluation complete"
            
        elif function_name == "identify_special_case":
            # Store special case identification in state
            if "coordination_status" not in state:
                updated_state["coordination_status"] = {}
            
            updated_state["coordination_status"]["special_case"] = function_args
            updated_state["coordination_status"]["is_special_case"] = function_args.get("is_special_case", False)
            
            # If escalation needed, update status
            if function_args.get("is_special_case", False):
                updated_state["status"] = "escalated"
            
            response = "Special case identification complete"
            
        elif function_name == "generate_status_update":
            # Store status update in state
            if "coordination_status" not in state:
                updated_state["coordination_status"] = {}
            
            updated_state["coordination_status"]["status_update"] = function_args
            updated_state["coordination_status"]["update_timestamp"] = datetime.datetime.now().isoformat()
            response = "Status update generated"
        
        return response, updated_state
    
    def evaluate_claim_status(self, claim_id: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate current status and determine next steps."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the status evaluation prompt
        prompt = f"""
        I need to evaluate the current status for claim {claim_id} and determine next steps.
        
        Current claim state: {json.dumps(state)}
        
        Please evaluate:
        1. What is the current status of the claim?
        2. What should be the next status in the workflow?
        3. What actions are required to move forward?
        4. Is any information missing that would block progress?
        5. What is the appropriate priority for this claim?
        6. Is escalation needed for any reason?
        
        Use the evaluate_claim_status function to record your evaluation.
        """
        
        try:
            # Generate the status evaluation
            response = chat.send_message(prompt)
            
            # Check for function calls
            evaluation_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "evaluate_claim_status":
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
                "current_status": state.get("status", "unknown"),
                "recommended_next_status": state.get("status", "unknown"),
                "required_actions": ["Review error in status evaluation"],
                "notes": f"Error evaluating claim status: {str(e)}"
            }
    
    def identify_special_case(self, claim_id: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Identify if claim requires special handling."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the special case identification prompt
        prompt = f"""
        I need to identify if claim {claim_id} requires special handling.
        
        Current claim state: {json.dumps(state)}
        
        Please identify:
        1. Is this a special case requiring non-standard handling?
        2. If so, what type of special case is it?
        3. What special handling instructions would be appropriate?
        4. What additional resources might be needed?
        5. What is the estimated resolution time for this case?
        
        Special cases might include:
        - High-value claims (>$100,000)
        - Claims with legal disputes or litigation
        - Claims with fraud indicators
        - Claims with severe injuries or fatalities
        - Claims with multiple parties or complex liability
        
        Use the identify_special_case function to record your findings.
        """
        
        try:
            # Generate the special case identification
            response = chat.send_message(prompt)
            
            # Check for function calls
            identification_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "identify_special_case":
                            identification_result = function_args
            
            # Return the identification result
            return {
                "claim_id": claim_id,
                "identification_timestamp": datetime.datetime.now().isoformat(),
                **identification_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "identification_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "is_special_case": False,
                "notes": f"Error identifying special case: {str(e)}"
            }
    
    def generate_status_update(self, claim_id: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a status update for the claim."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the status update prompt
        prompt = f"""
        I need to generate a status update for claim {claim_id}.
        
        Current claim state: {json.dumps(state)}
        
        Please provide:
        1. A summary of the current status
        2. An estimated percentage of completion for the claim process
        3. A description of the last activity on the claim
        4. The next steps in the process
        5. Any current blockers or issues
        6. An estimated completion date
        
        Use the generate_status_update function to record your update.
        """
        
        try:
            # Generate the status update
            response = chat.send_message(prompt)
            
            # Check for function calls
            update_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "generate_status_update":
                            update_result = function_args
            
            # Return the update result
            return {
                "claim_id": claim_id,
                "update_timestamp": datetime.datetime.now().isoformat(),
                **update_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "update_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "status_summary": f"Error generating status update: {str(e)}",
                "progress_percentage": 0,
                "next_steps": ["Review system error"]
            }
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state."""
        claim_id = state.get("claim_id")
        status = state.get("status")
        
        # Always evaluate status first
        status_evaluation = self.evaluate_claim_status(claim_id, state)
        if "coordination_status" not in state:
            state["coordination_status"] = {}
        
        state["coordination_status"]["status_evaluation"] = status_evaluation
        state["coordination_status"]["evaluation_timestamp"] = datetime.datetime.now().isoformat()
        
        # Check if special handling is needed
        special_case = self.identify_special_case(claim_id, state)
        state["coordination_status"]["special_case"] = special_case
        state["coordination_status"]["is_special_case"] = special_case.get("is_special_case", False)
        
        # If special case, update status
        if special_case.get("is_special_case", False):
            state["status"] = "escalated"
        # If not a special case, follow recommended status from evaluation
        elif status_evaluation.get("recommended_next_status") != state.get("status"):
            state["status"] = status_evaluation.get("recommended_next_status", state.get("status"))
        
        # Generate status update
        status_update = self.generate_status_update(claim_id, state)
        state["coordination_status"]["status_update"] = status_update
        state["coordination_status"]["update_timestamp"] = datetime.datetime.now().isoformat()
        
        # Update current agent
        state["current_agent"] = self.agent_name
        
        # Update timestamp
        state["updated_at"] = datetime.datetime.now().isoformat()
        
        return state
