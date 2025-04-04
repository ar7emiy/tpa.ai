# tests/unit/test_compliance_agent.py
import pytest
import json
import datetime
from agents.compliance_agent import ComplianceAgent

@pytest.fixture
def compliance_agent():
    """Create a compliance agent for testing."""
    return ComplianceAgent()

def test_agent_initialization(compliance_agent):
    """Test that the agent initializes correctly."""
    assert compliance_agent.agent_name == "ComplianceAgent"
    assert "Compliance Agent" in compliance_agent.system_prompt
    assert "Ensure all required documentation" in compliance_agent.system_prompt

def test_handle_function_call_verify_documentation(compliance_agent):
    """Test handling of documentation verification."""
    state = {}
    function_name = "verify_documentation"
    function_args = {
        "documentation_complete": True,
        "missing_documents": [],
        "incomplete_documents": [],
        "documentation_quality": "good",
        "notes": "All required documentation is present and complete"
    }
    
    response, updated_state = compliance_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "compliance_status" in updated_state
    assert "documentation" in updated_state["compliance_status"]
    assert updated_state["compliance_status"]["documentation"] == function_args

def test_handle_function_call_check_reporting_timeline(compliance_agent):
    """Test handling of reporting timeline check."""
    state = {}
    function_name = "check_reporting_timeline"
    function_args = {
        "timely_reporting": True,
        "incident_date": "2025-03-01T00:00:00Z",
        "employer_notification_date": "2025-03-01T14:30:00Z",
        "claim_filing_date": "2025-03-03T09:15:00Z",
        "statutory_deadline": "2025-05-01T00:00:00Z",
        "within_deadline": True,
        "delay_reason": "None - reported promptly"
    }
    
    response, updated_state = compliance_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "compliance_status" in updated_state
    assert "timeline" in updated_state["compliance_status"]
    assert updated_state["compliance_status"]["timeline"] == function_args

def test_handle_function_call_evaluate_compliance_status(compliance_agent):
    """Test handling of compliance status evaluation."""
    state = {}
    function_name = "evaluate_compliance_status"
    function_args = {
        "is_compliant": True,
        "non_compliance_issues": [],
        "needs_medical_info": False,
        "needs_employment_info": False,
        "regulatory_concerns": [],
        "compliance_actions": ["Proceed to decision"]
    }
    
    response, updated_state = compliance_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "compliance_status" in updated_state
    assert "overall_status" in updated_state["compliance_status"]
    assert updated_state["compliance_status"]["overall_status"] == function_args
    assert updated_state["compliance_status"]["is_compliant"] == True
    assert updated_state["compliance_status"]["needs_medical_info"] == False

def test_process_compliance_check(compliance_agent, monkeypatch):
    """Test processing a claim in compliance check status."""
    # Mock the verify_documentation method
    def mock_verify_documentation(claim_id, claim_data):
        return {
            "claim_id": claim_id,
            "verification_timestamp": datetime.datetime.now().isoformat(),
            "documentation_complete": True,
            "missing_documents": [],
            "documentation_quality": "good"
        }
    
    # Mock the check_reporting_timeline method
    def mock_check_reporting_timeline(claim_id, claim_data):
        return {
            "claim_id": claim_id,
            "check_timestamp": datetime.datetime.now().isoformat(),
            "timely_reporting": True,
            "within_deadline": True
        }
    
    # tests/unit/test_compliance_agent.py (continued)
    # Mock the evaluate_compliance method
    def mock_evaluate_compliance(claim_id, doc_verification, timeline_check):
        return {
            "claim_id": claim_id,
            "evaluation_timestamp": datetime.datetime.now().isoformat(),
            "is_compliant": True,
            "non_compliance_issues": [],
            "needs_medical_info": False,
            "compliance_actions": ["Proceed to decision"]
        }
    
    # Apply the monkeypatches
    monkeypatch.setattr(compliance_agent, "verify_documentation", mock_verify_documentation)
    monkeypatch.setattr(compliance_agent, "check_reporting_timeline", mock_check_reporting_timeline)
    monkeypatch.setattr(compliance_agent, "evaluate_compliance", mock_evaluate_compliance)
    
    # Create a test state
    state = {
        "claim_id": "test-claim-123",
        "status": "compliance_check",
        "claimant_info": {"name": "John Doe"},
        "employer_info": {"company_name": "Acme Corp"},
        "medical_records": [{"diagnosis": "Lumbar strain"}],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Process the state
    updated_state = compliance_agent.process(state)
    
    # Assert the state has been updated correctly
    assert "compliance_status" in updated_state
    assert "documentation" in updated_state["compliance_status"]
    assert "timeline" in updated_state["compliance_status"]
    assert "overall_status" in updated_state["compliance_status"]
    assert "is_compliant" in updated_state["compliance_status"]
    assert updated_state["status"] == "decision_pending"
    assert updated_state["current_agent"] == "ComplianceAgent"
