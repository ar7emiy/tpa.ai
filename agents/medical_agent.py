# agents/medical_agent.py
import datetime
import json
from typing import Dict, List, Any, Tuple
from .base_agent import BaseAgent
from google.generativeai.types import FunctionDeclaration, Tool

class MedicalAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.system_prompt = self._format_system_prompt(
            "Medical Assessment Agent",
            """Your responsibilities:
            1. Review medical documentation for accuracy and completeness
            2. Assess the severity and nature of reported injuries
            3. Evaluate treatment plans for appropriateness
            4. Determine reasonable work restrictions
            5. Estimate recovery timelines
            
            Base your assessments on medical best practices and workers' compensation guidelines.
            Be thorough, fair, and objective in your medical evaluations."""
        )
        
        # Define tools for this agent
        self.tools = [
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="analyze_medical_records",
                        description="Analyze medical records and provide assessment",
                        parameters={
                            "type": "object",
                            "properties": {
                                "diagnosis_confirmed": {"type": "boolean", "description": "Whether diagnosis is confirmed by medical evidence"},
                                "diagnosis_code": {"type": "string", "description": "Medical diagnosis code (ICD-10)"},
                                "injury_severity": {"type": "string", "description": "Assessment of injury severity (mild, moderate, severe)"},
                                "injury_description": {"type": "string", "description": "Detailed description of the injury"},
                                "causally_related": {"type": "boolean", "description": "Whether injury is causally related to reported incident"},
                                "pre_existing_conditions": {"type": "array", "items": {"type": "string"}, "description": "Any relevant pre-existing conditions"},
                                "treatment_appropriateness": {"type": "string", "description": "Assessment of treatment appropriateness"},
                                "additional_tests_needed": {"type": "array", "items": {"type": "string"}, "description": "Any additional tests or consultations needed"},
                                "notes": {"type": "string", "description": "Additional medical notes"}
                            },
                            "required": ["diagnosis_confirmed", "injury_severity", "causally_related"]
                        }
                    ),
                    FunctionDeclaration(
                        name="assess_work_restrictions",
                        description="Assess work restrictions based on medical condition",
                        parameters={
                            "type": "object",
                            "properties": {
                                "can_work": {"type": "boolean", "description": "Whether claimant can work in some capacity"},
                                "restriction_duration": {"type": "string", "description": "Expected duration of restrictions"},
                                "lifting_restrictions": {"type": "string", "description": "Lifting restrictions if any"},
                                "mobility_restrictions": {"type": "string", "description": "Mobility restrictions if any"},
                                "hours_restrictions": {"type": "string", "description": "Working hours restrictions if any"},
                                "special_accommodations": {"type": "string", "description": "Special accommodations needed"},
                                "estimated_recovery_time": {"type": "string", "description": "Estimated recovery time"},
                                "follow_up_date": {"type": "string", "description": "Recommended follow-up date (ISO format)"}
                            },
                            "required": ["can_work", "restriction_duration", "estimated_recovery_time"]
                        }
                    ),
                    FunctionDeclaration(
                        name="recommend_treatment_plan",
                        description="Recommend or assess treatment plan",
                        parameters={
                            "type": "object",
                            "properties": {
                                "recommended_treatments": {"type": "array", "items": {"type": "string"}, "description": "Recommended treatments"},
                                "estimated_duration": {"type": "string", "description": "Estimated treatment duration"},
                                "physical_therapy": {"type": "string", "description": "Physical therapy recommendations"},
                                "medications": {"type": "array", "items": {"type": "string"}, "description": "Recommended medications"},
                                "surgery_needed": {"type": "boolean", "description": "Whether surgery is needed"},
                                "specialist_referrals": {"type": "array", "items": {"type": "string"}, "description": "Specialist referrals needed"},
                                "expected_outcomes": {"type": "string", "description": "Expected outcomes of treatment"}
                            },
                            "required": ["recommended_treatments", "estimated_duration"]
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
        
        if function_name == "analyze_medical_records":
            # Store medical analysis in state
            if "medical_assessment" not in state:
                updated_state["medical_assessment"] = {}
            
            updated_state["medical_assessment"]["diagnosis"] = function_args
            updated_state["medical_assessment"]["assessment_timestamp"] = datetime.datetime.now().isoformat()
            response = "Medical record analysis complete"
            
        elif function_name == "assess_work_restrictions":
            # Store work restrictions in state
            if "medical_assessment" not in state:
                updated_state["medical_assessment"] = {}
            
            updated_state["medical_assessment"]["work_restrictions"] = function_args
            updated_state["work_restrictions"] = function_args
            response = "Work restrictions assessment complete"
            
        elif function_name == "recommend_treatment_plan":
            # Store treatment plan in state
            if "medical_assessment" not in state:
                updated_state["medical_assessment"] = {}
            
            updated_state["medical_assessment"]["treatment_plan"] = function_args
            updated_state["treatment_plan"] = function_args
            response = "Treatment plan recommendation complete"
        
        return response, updated_state
    
    def analyze_medical_records(self, claim_id: str, medical_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze medical records and provide assessment."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the medical analysis prompt
        prompt = f"""
        I need to analyze medical records for claim {claim_id}.
        
        Medical records: {json.dumps(medical_records)}
        
        Please analyze these records and provide:
        1. Assessment of the diagnosis and its confirmation by medical evidence
        2. Evaluation of the injury severity
        3. Determination if the injury is causally related to the reported incident
        4. Identification of any pre-existing conditions that may affect recovery
        5. Evaluation of the appropriateness of the current treatment
        
        Use the analyze_medical_records function to record your findings.
        """
        
        try:
            # Generate the medical analysis
            response = chat.send_message(prompt)
            
            # Check for function calls
            analysis_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "analyze_medical_records":
                            analysis_result = function_args
            
            # Return the analysis result
            return {
                "claim_id": claim_id,
                "analysis_timestamp": datetime.datetime.now().isoformat(),
                **analysis_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "analysis_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "diagnosis_confirmed": False,
                "injury_severity": "unknown",
                "causally_related": False,
                "notes": f"Error analyzing medical records: {str(e)}"
            }
    
    def assess_work_restrictions(self, claim_id: str, medical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess work restrictions based on medical condition."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the work restrictions prompt
        prompt = f"""
        I need to assess work restrictions for claim {claim_id} based on the medical analysis.
        
        Medical analysis: {json.dumps(medical_analysis)}
        
        Please determine:
        1. Whether the claimant can work in some capacity
        2. What specific work restrictions are appropriate
        3. How long these restrictions should be in place
        4. The estimated recovery time
        
        Use the assess_work_restrictions function to record your findings.
        """
        
        try:
            # Generate the work restrictions assessment
            response = chat.send_message(prompt)
            
            # Check for function calls
            restrictions_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "assess_work_restrictions":
                            restrictions_result = function_args
            
            # Return the restrictions result
            return {
                "claim_id": claim_id,
                "assessment_timestamp": datetime.datetime.now().isoformat(),
                **restrictions_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "assessment_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "can_work": False,
                "restriction_duration": "unknown",
                "estimated_recovery_time": "unknown",
                "notes": f"Error assessing work restrictions: {str(e)}"
            }
    
    def recommend_treatment_plan(self, claim_id: str, medical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend or assess treatment plan."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the treatment plan prompt
        prompt = f"""
        I need to recommend or assess a treatment plan for claim {claim_id} based on the medical analysis.
        
        Medical analysis: {json.dumps(medical_analysis)}
        
        Please provide:
        1. Recommended treatments
        2. Estimated treatment duration
        3. Whether physical therapy is needed and what type
        4. Appropriate medications
        5. Whether surgical intervention is needed
        6. Any specialist referrals required
        
        Use the recommend_treatment_plan function to record your recommendations.
        """
        
        try:
            # Generate the treatment plan
            response = chat.send_message(prompt)
            
            # Check for function calls
            treatment_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "recommend_treatment_plan":
                            treatment_result = function_args
            
            # Return the treatment plan
            return {
                "claim_id": claim_id,
                "recommendation_timestamp": datetime.datetime.now().isoformat(),
                **treatment_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "recommendation_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "recommended_treatments": ["Unable to determine appropriate treatments"],
                "estimated_duration": "unknown",
                "notes": f"Error recommending treatment plan: {str(e)}"
            }
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state."""
        claim_id = state.get("claim_id")
        status = state.get("status")
        
        if status == "medical_review":
            # Get medical records
            medical_records = state.get("medical_records", [])
            
            if not medical_records:
                # If no medical records, state remains unchanged
                return state
            
            # Analyze medical records
            medical_analysis = self.analyze_medical_records(claim_id, medical_records)
            
            # Update state with medical analysis
            if "medical_assessment" not in state:
                state["medical_assessment"] = {}
            
            state["medical_assessment"]["diagnosis"] = medical_analysis
            state["current_agent"] = self.agent_name
            
            # Assess work restrictions based on medical analysis
            work_restrictions = self.assess_work_restrictions(claim_id, medical_analysis)
            state["medical_assessment"]["work_restrictions"] = work_restrictions
            state["work_restrictions"] = work_restrictions
            
            # Recommend treatment plan
            treatment_plan = self.recommend_treatment_plan(claim_id, medical_analysis)
            state["medical_assessment"]["treatment_plan"] = treatment_plan
            state["treatment_plan"] = treatment_plan
            
            # Move to compliance check if medical assessment is complete
            if (medical_analysis.get("diagnosis_confirmed") is not None and 
                work_restrictions.get("can_work") is not None and 
                treatment_plan.get("recommended_treatments")):
                state["status"] = "compliance_check"
        
        # Update timestamp
        state["updated_at"] = datetime.datetime.now().isoformat()
        
        return state
