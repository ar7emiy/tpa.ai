# workflow/graph.py
from typing import Dict, Any, Literal
from langchain.graphs import StateGraph
from .states import ClaimState, ClaimStatus
from ..agents.coordinator_agent import CoordinatorAgent
from ..agents.conversational_agent import ConversationalAgent
from ..agents.verification_agent import VerificationAgent
from ..agents.medical_agent import MedicalAgent
from ..agents.compliance_agent import ComplianceAgent
from ..agents.decision_agent import DecisionAgent
from ..agents.payment_agent import PaymentAgent
from .transitions import WorkflowTransitionManager

def create_workflow():
    """Create the LangGraph workflow for claims processing."""
    # Initialize agents
    coordinator_agent = CoordinatorAgent()
    conversational_agent = ConversationalAgent()
    verification_agent = VerificationAgent()
    medical_agent = MedicalAgent()
    compliance_agent = ComplianceAgent()
    decision_agent = DecisionAgent()
    payment_agent = PaymentAgent()
    
    # Initialize transition manager
    transition_manager = WorkflowTransitionManager()
    
    # Create graph
    graph_builder = StateGraph(ClaimState)
    
    # Add agent nodes
    graph_builder.add_node("coordinator", coordinator_agent.process)
    graph_builder.add_node("conversational", conversational_agent.process)
    graph_builder.add_node("verification", verification_agent.process)
    graph_builder.add_node("medical", medical_agent.process)
    graph_builder.add_node("compliance", compliance_agent.process)
    graph_builder.add_node("decision", decision_agent.process)
    graph_builder.add_node("payment", payment_agent.process)
    
    # Define routing based on claim status
    def route_by_status(state: ClaimState) -> Literal[
        "coordinator", "conversational", "verification", 
        "medical", "compliance", "decision", "payment", "__end__"
    ]:
        status = state.get("status")
        
        # Route to the appropriate agent based on status
        if status == ClaimStatus.NEW:
            return "conversational"
        elif status == ClaimStatus.VERIFICATION:
            return "verification"
        elif status == ClaimStatus.MEDICAL_REVIEW:
            return "medical"
        elif status == ClaimStatus.COMPLIANCE_CHECK:
            return "compliance"
        elif status == ClaimStatus.DECISION_PENDING:
            return "decision"
        elif status in [ClaimStatus.APPROVED, ClaimStatus.PAYMENT_PROCESSING, ClaimStatus.RECOVERY_CHECK]:
            return "payment"
        elif status in [ClaimStatus.DENIED, ClaimStatus.CLOSED]:
            return "__end__"
        else:
            # Default to coordinator if status is unknown
            return "coordinator"
    
    # Add conditional edges from START to agents
    graph_builder.add_conditional_edges(
        "",
        route_by_status,
        {
            "coordinator": "coordinator",
            "conversational": "conversational",
            "verification": "verification",
            "medical": "medical",
            "compliance": "compliance",
            "decision": "decision",
            "payment": "payment",
            "__end__": None
        }
    )
    
    # After each agent processes, determine next state and route back
    def after_agent_processing(state: ClaimState) -> Literal["", "__end__"]:
        current_status = state.get("status")
        
        # If status is terminal, end processing
        if current_status in [ClaimStatus.CLOSED]:
            return "__end__"
        
        # Update status based on transition rules
        next_status, updated_state = transition_manager.get_next_state(current_status, state)
        
        # Update state with new status
        state["status"] = next_status
        for key, value in updated_state.items():
            if key not in state or value != state[key]:
                state[key] = value
        
        # Continue processing
        return ""
    
    # Connect all agent nodes back to the router
    for node in ["coordinator", "conversational", "verification", "medical", "compliance", "decision", "payment"]:
        graph_builder.add_conditional_edges(
            node,
            after_agent_processing,
            {
                "": "",
                "__end__": None
            }
        )
    
    # Compile the graph
    return graph_builder.compile()
