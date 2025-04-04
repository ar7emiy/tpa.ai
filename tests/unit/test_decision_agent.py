# tests/unit/test_decision_agent.py
import pytest
import json
import datetime
from agents.decision_agent import DecisionAgent

@pytest.fixture
def decision_agent():
    """Create a decision agent for testing."""
    return DecisionAgent()

def test_agent_initialization(decision_agent):
    """Test that the agent initializes correctly."""
    assert decision_agent.agent_name == "DecisionAgent"
    assert "Decision Agent" in decision_agent.system_prompt
    assert "Evaluate all evidence" in decision_agent.system_prompt

def test_handle_function_call_evaluate_evidence(decision_agent):
    """Test handling of evidence evaluation."""
    state = {}
    function_name = "evaluate_evidence"
    function_args = {
        "evidence_sufficient": True,
        "work_relatedness": "confirmed",
        "key_supporting_factors": ["Witness confirmation", "Medical diagnosis consistent with reported mechanism"],
        "key_contradicting_factors": [],
        "credibility_issues": [],
        "evidence_gaps": ["No prior medical records available for comparison"]
    }
    
    response, updated_state = decision_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "decision_status" in updated_state
    assert "evidence_evaluation" in updated_state["decision_status"]
    assert updated_state["decision_status"]["evidence_evaluation"] == function_args

def test_handle_function_call_determine_compensability(decision_agent):
    """Test handling of compensability determination."""
    state = {}
    function_name = "determine_compensability"
    function_args = {
        "compensable": True,
        "compensability_factors": ["Injury arose out of and in course of employment", "Timely reported"],
        "legal_basis": "State workers' compensation statute",
        "jurisdictional_requirements_met": True,
        "statutory_exclusions": []
    }
    
    response, updated_state = decision_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "decision_status" in updated_state
    assert "compensability" in updated_state["decision_status"]
    assert updated_state["decision_status"]["compensability"] == function_args

def test_handle_function_call_make_claim_decision(decision_agent):
    """Test handling of claim decision."""
    state = {}
    function_name = "make_claim_decision"
    function_args = {
        "approved": True,
        "decision_date": datetime.datetime.now().isoformat(),
        "effective_date": datetime.datetime.now().isoformat(),
        "reasoning": "Evidence supports work-related injury with appropriate treatment plan",
        "benefit_type": "Temporary total disability",
        "denial_reason": "",
        "appeal_rights": "Claimant has 30 days to appeal if dissatisfied with this decision"
    }
    
    response, updated_state = decision_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "decision_status" in updated_state
    assert "decision" in updated_state["decision_status"]
    assert updated_state["decision_status"]["approved"] == True
    assert "reasoning" in updated_state["decision_status"]

def test_handle_function_call_calculate_compensation(decision_agent):
    """Test handling of compensation calculation."""
    state = {}
    function_name = "calculate_compensation"
    function_args = {
        "compensation_type": "Temporary total disability",
        "weekly_amount": 800.00,
        "calculation_basis": "2/3 of average weekly wage of $1,200",
        "estimated_duration": "6 weeks",
        "maximum_benefit": 4800.00,
        "waiting_period": "3 days",
        "retroactive_amount": 0
    }
    
    response, updated_state = decision_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "decision_status" in updated_state
    assert "compensation" in updated_state["decision_status"]
    assert updated_state["decision_status"]["weekly_amount"] == 800.00

def test_process_decision_pending(decision_agent, monkeypatch):
    """Test processing a claim in decision pending status."""
    # Mock the evaluate_evidence method
    def mock_evaluate_evidence(claim_id, claim_data):
        return {
            "claim_id": claim_id,
            "evaluation_timestamp": datetime.datetime.now().isoformat(),
            "evidence_sufficient": True,
            "work_relatedness": "confirmed",
            "key_supporting_factors": ["Consistent medical evidence"]
        }
    
    # Mock the determine_compensability method
    def mock_determine_compensability(claim_id, evidence_evaluation):
        return {
            "claim_id": claim_id,
            "determination_timestamp": datetime.datetime.now().isoformat(),
            "compensable": True,
            "compensability_factors": ["Work-related injury"]
        }
    
    # Mock the make_claim_decision method
    def mock_make_claim_decision(claim_id, evidence_evaluation, compensability):
        return {
            "claim_id": claim_id,
            "approved": True,
            "decision_date": datetime.datetime.now().isoformat(),
            "reasoning": "Evidence supports compensable claim"
        }
    
    # Mock the calculate_compensation method
    def mock_calculate_compensation(claim_id, claim_data, decision):
        return {
            "claim_id": claim_id,
            "calculation_timestamp": datetime.datetime.now().isoformat(),
            "compensation_type": "Temporary total disability",
            "weekly_amount": 800.00,
            "estimated_duration": "6 weeks"
        }
    
    # Apply the monkeypatches
    monkeypatch.setattr(decision_agent, "evaluate_evidence", mock_evaluate_evidence)
    monkeypatch.setattr(decision_agent, "determine_compensability", mock_determine_compensability)
    monkeypatch.setattr(decision_agent, "make_claim_decision", mock_make_claim_decision)
    monkeypatch.setattr(decision_agent, "calculate_compensation", mock_calculate_compensation)
    
    # Create a test state
    state = {
        "claim_id": "test-claim-123",
        "status": "decision_pending",
        "claimant_info": {"name": "John Doe"},
        "employer_info": {"company_name": "Acme Corp"},
        "medical_records": [{"diagnosis": "Lumbar strain"}],
        "medical_assessment": {"diagnosis": {"causally_related": True}},
        "verification_status": {"employment_verified": True},
        "compliance_status": {"is_compliant": True},
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Process the state
    updated_state = decision_agent.process(state)
    
    # Assert the state has been updated correctly
    assert "decision_status" in updated_state
    assert "evidence_evaluation" in updated_state["decision_status"]
    assert "compensability" in updated_state["decision_status"]
    assert "decision" in updated_state["decision_status"]
    assert "compensation" in updated_state["decision_status"]
    assert updated_state["decision_status"]["approved"] == True
    assert updated_state["decision_status"]["weekly_amount"] == 800.00
    assert updated_state["status"] == "approved"
    assert updated_state["current_agent"] == "DecisionAgent"
