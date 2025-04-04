# tests/unit/test_coordinator_agent.py
import pytest
import json
import datetime
from agents.coordinator_agent import CoordinatorAgent

@pytest.fixture
def coordinator_agent():
    """Create a coordinator agent for testing."""
    return CoordinatorAgent()

def test_agent_initialization(coordinator_agent):
    """Test that the agent initializes correctly."""
    assert coordinator_agent.agent_name == "CoordinatorAgent"
    assert "Coordinator Agent" in coordinator_agent.system_prompt
    assert "Orchestrate the overall" in coordinator_agent.system_prompt

def test_handle_function_call_evaluate_claim_status(coordinator_agent):
    """Test handling of claim status evaluation."""
    state = {}
    function_name = "evaluate_claim_status"
    function_args = {
        "current_status": "verification",
        "recommended_next_status": "medical_review",
        "required_actions": ["Complete employment verification"],
        "missing_information": ["Medical records"],
        "priority": "normal",
        "escalation_needed": False,
        "notes": "Proceed with normal workflow"
    }
    
    response, updated_state = coordinator_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "coordination_status" in updated_state
    assert "status_evaluation" in updated_state["coordination_status"]
    assert updated_state["coordination_status"]["status_evaluation"] == function_args
    assert "evaluation_timestamp" in updated_state["coordination_status"]

def test_handle_function_call_identify_special_case(coordinator_agent):
    """Test handling of special case identification."""
    state = {}
    function_name = "identify_special_case"
    function_args = {
        "is_special_case": True,
        "case_type": "high-value",
        "handling_instructions": "Require supervisory review of all decisions",
        "additional_resources_needed": ["Legal consultation", "Medical specialist review"],
        "estimated_resolution_time": "60 days"
    }
    
    response, updated_state = coordinator_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "coordination_status" in updated_state
    assert "special_case" in updated_state["coordination_status"]
    assert updated_state["coordination_status"]["special_case"] == function_args
    assert updated_state["coordination_status"]["is_special_case"] == True
    assert updated_state["status"] == "escalated"

def test_handle_function_call_generate_status_update(coordinator_agent):
    """Test handling of status update generation."""
    state = {}
    function_name = "generate_status_update"
    function_args = {
        "status_summary": "Claim is in verification stage with employment confirmed",
        "progress_percentage": 25,
        "last_activity": "Employment verification completed on 2023-04-01",
        "next_steps": ["Medical records review", "Compliance check"],
        "blockers": ["Waiting for medical documentation from provider"],
        "estimated_completion": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
    }
    
    response, updated_state = coordinator_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "coordination_status" in updated_state
    assert "status_update" in updated_state["coordination_status"]
    assert updated_state["coordination_status"]["status_update"] == function_args
    assert "update_timestamp" in updated_state["coordination_status"]

def test_process_coordination(coordinator_agent, monkeypatch):
    """Test processing coordination for a claim."""
    # Mock the evaluate_claim_status method
    def mock_evaluate_claim_status(claim_id, state):
        return {
            "claim_id": claim_id,
            "evaluation_timestamp": datetime.datetime.now().isoformat(),
            "current_status": state.get("status", "unknown"),
            "recommended_next_status": "medical_review",
            "required_actions": ["Obtain medical records"],
            "priority": "normal",
            "escalation_needed": False
        }
    
    # Mock the identify_special_case method
    def mock_identify_special_case(claim_id, state):
        return {
            "claim_id": claim_id,
            "identification_timestamp": datetime.datetime.now().isoformat(),
            "is_special_case": False,
            "case_type": "",
            "handling_instructions": ""
        }
    
    # Mock the generate_status_update method
    def mock_generate_status_update(claim_id, state):
        return {
            "claim_id": claim_id,
            "update_timestamp": datetime.datetime.now().isoformat(),
            "status_summary": "Claim is progressing normally",
            "progress_percentage": 30,
            "next_steps": ["Medical review"]
        }
    
    # Apply the monkeypatches
    monkeypatch.setattr(coordinator_agent, "evaluate_claim_status", mock_evaluate_claim_status)
    monkeypatch.setattr(coordinator_agent, "identify_special_case", mock_identify_special_case)
    monkeypatch.setattr(coordinator_agent, "generate_status_update", mock_generate_status_update)
    
    # Create a test state
    state = {
        "claim_id": "test-claim-123",
        "status": "verification",
        "claimant_info": {"name": "John Doe"},
        "employer_info": {"company_name": "Acme Corp"},
        "verification_status": {"employment_verified": True},
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Process the state
    updated_state = coordinator_agent.process(state)
    
    # Assert the state has been updated correctly
    assert "coordination_status" in updated_state
    assert "status_evaluation" in updated_state["coordination_status"]
    assert "special_case" in updated_state["coordination_status"]
    assert "status_update" in updated_state["coordination_status"]
    assert updated_state["status"] == "medical_review"
    assert updated_state["current_agent"] == "CoordinatorAgent"
