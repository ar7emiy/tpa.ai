# agents/payment_agent.py
import datetime
import json
from typing import Dict, List, Any, Tuple
from .base_agent import BaseAgent
from google.generativeai.types import FunctionDeclaration, Tool

class PaymentAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.system_prompt = self._format_system_prompt(
            "Payment Agent",
            """Your responsibilities:
            1. Process payments for approved claims
            2. Calculate payment amounts based on compensation determination
            3. Track payment history and schedule future payments
            4. Monitor recovery progress
            5. Adjust payments based on changes in condition
            6. Finalize payments when recovery is complete
            
            Be accurate, efficient, and thorough in payment processing and tracking."""
        )
        
        # Define tools for this agent
        self.tools = [
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="process_payment",
                        description="Process a payment for an approved claim",
                        parameters={
                            "type": "object",
                            "properties": {
                                "payment_amount": {"type": "number", "description": "Payment amount"},
                                "payment_type": {"type": "string", "description": "Type of payment (initial, recurring, final)"},
                                "payment_date": {"type": "string", "description": "Date of payment (ISO format)"},
                                "payment_period": {"type": "string", "description": "Period covered by payment"},
                                "payment_method": {"type": "string", "description": "Method of payment"},
                                "notes": {"type": "string", "description": "Additional payment notes"}
                            },
                            "required": ["payment_amount", "payment_type", "payment_date"]
                        }
                    ),
                    FunctionDeclaration(
                        name="schedule_future_payments",
                        description="Schedule future payments for an approved claim",
                        parameters={
                            "type": "object",
                            "properties": {
                                "payment_schedule": {"type": "array", "items": {
                                    "type": "object",
                                    "properties": {
                                        "scheduled_date": {"type": "string", "description": "Scheduled payment date (ISO format)"},
                                        "estimated_amount": {"type": "number", "description": "Estimated payment amount"},
                                        "payment_type": {"type": "string", "description": "Type of payment"}
                                    }
                                }, "description": "Schedule of future payments"},
                                "payment_frequency": {"type": "string", "description": "Frequency of payments (weekly, bi-weekly, monthly)"},
                                "next_review_date": {"type": "string", "description": "Date to review payment schedule (ISO format)"}
                            },
                            "required": ["payment_schedule", "payment_frequency"]
                        }
                    ),
                    FunctionDeclaration(
                        name="track_recovery",
                        description="Track recovery progress and assess continued eligibility",
                        parameters={
                            "type": "object",
                            "properties": {
                                "recovery_status": {"type": "string", "description": "Current recovery status (improving, stable, worsening)"},
                                "work_status": {"type": "string", "description": "Current work status (off work, light duty, full duty)"},
                                "fully_recovered": {"type": "boolean", "description": "Whether claimant has fully recovered"},
                                "recovery_date": {"type": "string", "description": "Date of full recovery, if applicable (ISO format)"},
                                "continuing_treatment": {"type": "boolean", "description": "Whether claimant is still receiving treatment"},
                                "next_medical_review": {"type": "string", "description": "Date of next medical review (ISO format)"},
                                "notes": {"type": "string", "description": "Additional recovery notes"}
                            },
                            "required": ["recovery_status", "work_status"]
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
        
        if function_name == "process_payment":
            # Store payment in state
            if "payment_status" not in state:
                updated_state["payment_status"] = {}
            
            if "payments" not in state.get("payment_status", {}):
                if "payment_status" not in updated_state:
                    updated_state["payment_status"] = {}
                updated_state["payment_status"]["payments"] = []
            
            # Add new payment to the list
            payments = state.get("payment_status", {}).get("payments", [])
            updated_payments = payments + [function_args]
            updated_state["payment_status"]["payments"] = updated_payments
            updated_state["payment_status"]["last_payment_date"] = function_args.get("payment_date")
            updated_state["payment_status"]["payment_processed"] = True
            response = "Payment processed successfully"
            
        elif function_name == "schedule_future_payments":
            # Store payment schedule in state
            if "payment_status" not in state:
                updated_state["payment_status"] = {}
            
            updated_state["payment_status"]["payment_schedule"] = function_args.get("payment_schedule", [])
            updated_state["payment_status"]["payment_frequency"] = function_args.get("payment_frequency")
            updated_state["payment_status"]["next_review_date"] = function_args.get("next_review_date")
            response = "Future payments scheduled"
            
        elif function_name == "track_recovery":
            # Store recovery status in state
            if "recovery_status" not in state:
                updated_state["recovery_status"] = {}
            
            updated_state["recovery_status"] = function_args
            updated_state["recovery_status"]["assessment_date"] = datetime.datetime.now().isoformat()
            response = "Recovery status updated"
        
        return response, updated_state
    
    def process_initial_payment(self, claim_id: str, decision_status: Dict[str, Any]) -> Dict[str, Any]:
        """Process the initial payment for an approved claim."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the payment processing prompt
        prompt = f"""
        I need to process the initial payment for approved claim {claim_id}.
        
        Decision status: {json.dumps(decision_status)}
        
        Please:
        1. Determine the appropriate initial payment amount
        2. Specify the payment type
        3. Set the payment date
        4. Indicate the period covered by this payment
        5. Add any relevant notes for this payment
        
        Use the process_payment function to record the payment.
        """
        
        try:
            # Generate the payment processing
            response = chat.send_message(prompt)
            
            # Check for function calls
            payment_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "process_payment":
                            payment_result = function_args
            
            # Return the payment result
            return {
                "claim_id": claim_id,
                "processing_timestamp": datetime.datetime.now().isoformat(),
                **payment_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "processing_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "payment_amount": 0,
                "payment_type": "initial",
                "payment_date": datetime.datetime.now().isoformat(),
                "notes": f"Error processing payment: {str(e)}"
            }
    
    def schedule_payments(self, claim_id: str, decision_status: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule future payments for an approved claim."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the payment scheduling prompt
        prompt = f"""
        I need to schedule future payments for approved claim {claim_id}.
        
        Decision status: {json.dumps(decision_status)}
        
        Please:
        1. Create a schedule of future payments with dates and amounts
        2. Specify the payment frequency
        3. Set a date for the next review of the payment schedule
        
        Use the schedule_future_payments function to record the schedule.
        """
        
        try:
            # Generate the payment schedule
            response = chat.send_message(prompt)
            
            # Check for function calls
            schedule_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "schedule_future_payments":
                            schedule_result = function_args
            
            # Return the schedule result
            return {
                "claim_id": claim_id,
                "scheduling_timestamp": datetime.datetime.now().isoformat(),
                **schedule_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "scheduling_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "payment_schedule": [],
                "payment_frequency": "unknown",
                "next_review_date": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
                "notes": f"Error scheduling payments: {str(e)}"
            }
    
    def assess_recovery(self, claim_id: str, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess recovery progress and continued eligibility."""
        # Start a chat with Gemini
        chat = self.model.start_chat()
        
        # Create the recovery assessment prompt
        prompt = f"""
        I need to assess recovery progress for claim {claim_id}.
        
        Claim data: {json.dumps(claim_data)}
        
        Please assess:
        1. What is the current recovery status?
        2. What is the current work status?
        3. Has the claimant fully recovered?
        4. Is continuing treatment needed?
        5. When should the next medical review occur?
        
        Use the track_recovery function to record your assessment.
        """
        
        try:
            # Generate the recovery assessment
            response = chat.send_message(prompt)
            
            # Check for function calls
            recovery_result = {}
            if hasattr(response, "candidates") and hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "function_call"):
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = json.loads(function_call.args)
                        
                        if function_name == "track_recovery":
                            recovery_result = function_args
            
            # Return the recovery result
            return {
                "claim_id": claim_id,
                "assessment_timestamp": datetime.datetime.now().isoformat(),
                **recovery_result
            }
        except Exception as e:
            return {
                "claim_id": claim_id,
                "assessment_timestamp": datetime.datetime.now().isoformat(),
                "error": str(e),
                "recovery_status": "unknown",
                "work_status": "unknown",
                "fully_recovered": False,
                "continuing_treatment": True,
                "next_medical_review": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
                "notes": f"Error assessing recovery: {str(e)}"
            }
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state."""
        claim_id = state.get("claim_id")
        status = state.get("status")
        
        # Extract relevant claim data
        claim_data = {
            "claimant_info": state.get("claimant_info", {}),
            "medical_assessment": state.get("medical_assessment", {}),
            "decision_status": state.get("decision_status", {}),
            "payment_status": state.get("payment_status", {}),
            "work_restrictions": state.get("work_restrictions", {}),
            "treatment_plan": state.get("treatment_plan", {}),
            "recovery_status": state.get("recovery_status", {})
        }
        
        # Process based on status
        if status == "approved":
            # Initial approval - process first payment
            decision_status = state.get("decision_status", {})
            
            # Process initial payment
            payment_result = self.process_initial_payment(claim_id, decision_status)
            if "payment_status" not in state:
                state["payment_status"] = {}
            
            if "payments" not in state["payment_status"]:
                state["payment_status"]["payments"] = []
            
            # Add payment to list
            state["payment_status"]["payments"].append(payment_result)
            state["payment_status"]["last_payment_date"] = payment_result.get("payment_date")
            state["payment_status"]["payment_processed"] = True
            
            # Schedule future payments
            schedule_result = self.schedule_payments(claim_id, decision_status)
            state["payment_status"]["payment_schedule"] = schedule_result.get("payment_schedule", [])
            state["payment_status"]["payment_frequency"] = schedule_result.get("payment_frequency")
            state["payment_status"]["next_review_date"] = schedule_result.get("next_review_date")
            
            # Update status to payment processing
            state["status"] = "payment_processing"
            state["current_agent"] = self.agent_name
            
        elif status == "payment_processing":
            # Continuing payments - assess recovery
            recovery_assessment = self.assess_recovery(claim_id, claim_data)
            state["recovery_status"] = recovery_assessment
            
            # Update status based on recovery
            if recovery_assessment.get("fully_recovered", False):
                # If fully recovered, process final payment and close
                final_payment = {
                    "payment_amount": state["decision_status"].get("weekly_amount", 0),
                    "payment_type": "final",
                    "payment_date": datetime.datetime.now().isoformat(),
                    "payment_period": "final settlement",
                    "notes": "Final payment - claim closed due to full recovery"
                }
                
                if "payments" not in state["payment_status"]:
                    state["payment_status"]["payments"] = []
                
                state["payment_status"]["payments"].append(final_payment)
                state["payment_status"]["last_payment_date"] = final_payment.get("payment_date")
                state["status"] = "closed"
            else:
                # If not fully recovered, continue payment cycle
                # Find the next scheduled payment
                schedule = state["payment_status"].get("payment_schedule", [])
                if schedule:
                    next_payment = min(schedule, key=lambda x: x.get("scheduled_date", "9999-12-31"))
                    
                    # If next payment is due (scheduled date is in the past)
                    if next_payment.get("scheduled_date", "") <= datetime.datetime.now().isoformat():
                        payment = {
                            "payment_amount": next_payment.get("estimated_amount", 0),
                            "payment_type": "recurring",
                            "payment_date": datetime.datetime.now().isoformat(),
                            "payment_period": f"continuing benefits - {next_payment.get('payment_type', 'standard')}",
                            "notes": "Regularly scheduled payment"
                        }
                        
                        if "payments" not in state["payment_status"]:
                            state["payment_status"]["payments"] = []
                        
                        state["payment_status"]["payments"].append(payment)
                        state["payment_status"]["last_payment_date"] = payment.get("payment_date")
                        
                        # Remove processed payment from schedule
                        state["payment_status"]["payment_schedule"] = [
                            p for p in schedule if p.get("scheduled_date") != next_payment.get("scheduled_date")
                        ]
                
                # Check if it's time for review
                if state["payment_status"].get("next_review_date", "9999-12-31") <= datetime.datetime.now().isoformat():
                    # Re-schedule payments based on current status
                    schedule_result = self.schedule_payments(claim_id, claim_data)
                    state["payment_status"]["payment_schedule"] = schedule_result.get("payment_schedule", [])
                    state["payment_status"]["next_review_date"] = schedule_result.get("next_review_date")
                
                state["status"] = "recovery_check"
        
        elif status == "recovery_check":
            # Check recovery status
            recovery_assessment = self.assess_recovery(claim_id, claim_data)
            state["recovery_status"] = recovery_assessment
            
            # Update status based on recovery
            if recovery_assessment.get("fully_recovered", False):
                # If fully recovered, process final payment and close
                final_payment = {
                    "payment_amount": state["decision_status"].get("weekly_amount", 0),
                    "payment_type": "final",
                    "payment_date": datetime.datetime.now().isoformat(),
                    "payment_period": "final settlement",
                    "notes": "Final payment - claim closed due to full recovery"
                }
                
                if "payments" not in state["payment_status"]:
                    state["payment_status"]["payments"] = []
                
                state["payment_status"]["payments"].append(final_payment)
                state["payment_status"]["last_payment_date"] = final_payment.get("payment_date")
                state["status"] = "closed"
            else:
                # Continue payment processing
                state["status"] = "payment_processing"
        
        # Update timestamp
        state["updated_at"] = datetime.datetime.now().isoformat()
        
        return state
