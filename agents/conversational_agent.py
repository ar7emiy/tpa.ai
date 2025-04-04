# agents/conversational_agent.py
import datetime
import json
from typing import Dict, List, Any, Tuple
from .base_agent import BaseAgent
from google.generativeai.types import FunctionDeclaration, Tool

class ConversationalAgent(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.0-pro"):
        super().__init__(model_name)
        self.system_prompt = self._format_system_prompt(
            "Conversational Agent",
            """Your responsibilities:
            1. Engage in conversations with stakeholders (claimant, employer, medical providers)
            2. Extract relevant information from conversations
            3. Ask appropriate follow-up questions to gather complete information
            4. Structure extracted information for other agents to use
            
            Be conversational, empathetic, and thorough in your information gathering."""
        )
        
        # Define tools for this agent
        self.tools = [
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="extract_claimant_data",
                        description="Extract structured claimant data from conversation",
                        parameters={
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Claimant's full name"},
                                "contact_info": {"type": "string", "description": "Contact information"},
                                "injury_date": {"type": "string", "description": "Date of injury (ISO format)"},
                                "injury_location": {"type": "string", "description": "Location where injury occurred"},
                                "injury_description": {"type": "string", "description": "Description of the injury"},
                                "how_it_occurred": {"type": "string", "description": "How the injury occurred"},
                                "witnesses": {"type": "array", "items": {"type": "string"}, "description": "Names of witnesses"},
                                "medical_attention": {"type": "boolean", "description": "Whether medical attention was sought"},
                                "medical_provider": {"type": "string", "description": "Medical provider if applicable"}
                            },
                            "required": ["name", "injury_date", "injury_description", "how_it_occurred"]
                        }
                    ),
                    FunctionDeclaration(
                        name="extract_employer_data",
                        description="Extract structured employer data from conversation",
                        parameters={
                            "type": "object",
                            "properties": {
                                "company_name": {"type": "string", "description": "Employer's company name"},
                                "supervisor_name": {"type": "string", "description": "Supervisor's name"},
                                "contact_info": {"type": "string", "description": "Contact information"},
                                "employment_duration": {"type": "string", "description": "How long claimant has been employed"},
                                "job_title": {"type": "string", "description": "Claimant's job title"},
                                "incident_reported": {"type": "boolean", "description": "Whether incident was reported to employer"},
                                "report_date": {"type": "string", "description": "Date incident was reported (ISO format)"}
                            },
                            "required": ["company_name"]
                        }
                    ),
                    FunctionDeclaration(
                        name="extract_medical_data",
                        description="Extract structured medical data from conversation with provider",
                        parameters={
                            "type": "object",
                            "properties": {
                                "provider_name": {"type": "string", "description": "Medical provider's name"},
                                "facility": {"type": "string", "description": "Medical facility name"},
                                "diagnosis": {"type": "string", "description": "Medical diagnosis"},
                                "treatment_plan": {"type": "string", "description": "Recommended treatment plan"},
                                "work_restrictions": {"type": "string", "description": "Work restrictions if any"},
                                "estimated_recovery": {"type": "string", "description": "Estimated recovery time"},
                                "follow_up_date": {"type": "string", "description": "Follow-up appointment date (ISO format)"}
                            },
                            "required": ["provider_name", "diagnosis"]
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
        
        if function_name == "extract_claimant_data":
            # Store extracted claimant data in state
            updated_state["claimant_info"] = function_args
            response = "Successfully extracted claimant data"
            
        elif function_name == "extract_employer_data":
            # Store extracted employer data in state
            updated_state["employer_info"] = function_args
            response = "Successfully extracted employer data"
            
        elif function_name == "extract_medical_data":
            # Store extracted medical data in state
            if "medical_records" not in state:
                updated_state["medical_records"] = []
            updated_state["medical_records"] = state.get("medical_records", []) + [function_args]
            response = "Successfully extracted medical data"
            
        return response, updated_state
    
    def simulate_conversation(self, role: str, claim_context: Dict, conversation_goal: str) -> Dict:
        """Simulate a conversation with a stakeholder to extract information."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the simulation prompt
        prompt = f"""
        You need to simulate a conversation with a {role} regarding claim {claim_context.get('claim_id', 'unknown')}.
        
        Claim context: {json.dumps(claim_context)}
        
        Goal of conversation: {conversation_goal}
        
        Please simulate both sides of this conversation (both you asking questions and the {role} responding).
        After the conversation, extract the key information obtained using the appropriate function.
        """
        
        # Generate the simulated conversation
        response = chat.send_message(prompt)
        
        # Check for function calls
        extracted_data = {}
        if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call"):
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = json.loads(function_call.args)
                    
                    # Handle the function call
                    _, updated_state = self.handle_function_call(
                        function_name, function_args, claim_context
                    )
                    extracted_data = next(iter(updated_state.values()))
        
        # Return the conversation and extracted data
        return {
            "conversation_text": response.text,
            "extracted_data": extracted_data,
            "stakeholder_type": role,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state."""
        claim_id = state.get("claim_id")
        status = state.get("status")
        
        # Determine which stakeholder to interact with based on status
        if status == "new":
            # New claim - interact with claimant
            conversation_result = self.simulate_conversation(
                "claimant", 
                {"claim_id": claim_id},
                "initial claim information gathering"
            )
            
            # Update state with conversation and extracted data
            if "conversations" not in state:
                state["conversations"] = {}
            if "claimant" not in state["conversations"]:
                state["conversations"]["claimant"] = []
                
            state["conversations"]["claimant"].append(conversation_result)
            state["claimant_info"] = conversation_result.get("extracted_data", {})
            state["current_agent"] = self.agent_name
            
            # Move to employer verification if claimant data was extracted
            if state["claimant_info"]:
                # Simulate conversation with employer for verification
                employer_conversation = self.simulate_conversation(
                    "employer",
                    {"claim_id": claim_id, "claimant_info": state["claimant_info"]},
                    "verify employment and incident details"
                )
                
                # Update state with employer conversation
                if "employer" not in state["conversations"]:
                    state["conversations"]["employer"] = []
                    
                state["conversations"]["employer"].append(employer_conversation)
                state["employer_info"] = employer_conversation.get("extracted_data", {})
                
                # Update status to verification
                state["status"] = "verification"
        
        elif status == "medical_review" and not state.get("medical_records"):
            # Need medical information - interact with medical provider
            medical_conversation = self.simulate_conversation(
                "medical_provider",
                {"claim_id": claim_id, "claimant_info": state.get("claimant_info", {})},
                "gather medical diagnosis, treatment, and work restrictions"
            )
            
            # Update state with medical conversation
            if "medical_provider" not in state["conversations"]:
                state["conversations"]["medical_provider"] = []
                
            state["conversations"]["medical_provider"].append(medical_conversation)
            
            if "medical_records" not in state:
                state["medical_records"] = []
            
            state["medical_records"].append(medical_conversation.get("extracted_data", {}))
        
        # Update timestamp
        state["updated_at"] = datetime.datetime.now().isoformat()
        
        return state
