# tests/unit/test_medical_agent.py
import pytest
import json
import datetime
from agents.medical_agent import MedicalAgent

@pytest.fixture
def medical_agent():
    """Create a medical agent for testing."""
    return MedicalAgent()

def test_agent_initialization(medical_agent):
    """Test that the agent initializes correctly."""
    assert medical_agent.agent_name == "MedicalAgent"
    assert "Medical Assessment Agent" in medical_agent.system_prompt
    assert "Review medical documentation" in medical_agent.system_prompt

def test_handle_function_call_analyze_medical_records(medical_agent):
    """Test handling of medical records analysis."""
    state = {}
    function_name = "analyze_medical_records"
    function_args = {
        "diagnosis_confirmed": True,
        "diagnosis_code": "S33.5",
        "injury_severity": "moderate",
        "injury_description": "Lumbar strain with mild radiculopathy",
        "causally_related": True,
        "pre_existing_conditions": ["Mild degenerative disc disease"],
        "treatment_appropriateness": "Appropriate conservative care",
        "additional_tests_needed": ["MRI if no improvement in 4 weeks"],
        "notes": "Patient should respond well to conservative treatment"
    }
    
    response, updated_state = medical_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "medical_assessment" in updated_state
    assert "diagnosis" in updated_state["medical_assessment"]
    assert updated_state["medical_assessment"]["diagnosis"] == function_args

def test_handle_function_call_assess_work_restrictions(medical_agent):
    """Test handling of work restrictions assessment."""
    state = {}
    function_name = "assess_work_restrictions"
    function_args = {
        "can_work": True,
        "restriction_duration": "4 weeks",
        "lifting_restrictions": "No lifting over 20 lbs",
        "mobility_restrictions": "Limited bending and twisting",
        "hours_restrictions": "8 hour shifts with regular breaks",
        "special_accommodations": "Ergonomic chair required",
        "estimated_recovery_time": "6-8 weeks",
        "follow_up_date": "2025-04-30T00:00:00Z"
    }
    
    response, updated_state = medical_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "medical_assessment" in updated_state
    assert "work_restrictions" in updated_state["medical_assessment"]
    assert "work_restrictions" in updated_state
    assert updated_state["work_restrictions"] == function_args

def test_handle_function_call_recommend_treatment_plan(medical_agent):
    """Test handling of treatment plan recommendation."""
    state = {}
    function_name = "recommend_treatment_plan"
    function_args = {
        "recommended_treatments": ["Physical therapy", "NSAIDs", "Muscle relaxants"],
        "estimated_duration": "6 weeks",
        "physical_therapy": "2x weekly for 6 weeks",
        "medications": ["Ibuprofen 800mg TID", "Cyclobenzaprine 10mg QHS"],
        "surgery_needed": False,
        "specialist_referrals": [],
        "expected_outcomes": "Full recovery with minimal residual symptoms"
    }
    
    response, updated_state = medical_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "medical_assessment" in updated_state
    assert "treatment_plan" in updated_state["medical_assessment"]
    assert "treatment_plan" in updated_state
    assert updated_state["treatment_plan"] == function_args

def test_process_medical_review(medical_agent, monkeypatch):
    """Test processing a claim in medical review status."""
    # Mock the analyze_medical_records method
    def mock_analyze_medical_records(claim_id, medical_records):
        return {
            "claim_id": claim_id,
            "analysis_timestamp": datetime.datetime.now().isoformat(),
            "diagnosis_confirmed": True,
            "injury_severity": "moderate",
            "causally_related": True,
            "notes": "Test analysis"
        }
    
    # Mock the assess_work_restrictions method
    def mock_assess_work_restrictions(claim_id, medical_analysis):
        return {
            "claim_id": claim_id,
            "assessment_timestamp": datetime.datetime.now().isoformat(),
            "can_work": True,
            "restriction_duration": "4 weeks",
            "estimated_recovery_time": "6 weeks"
        }
    
    # Mock the recommend_treatment_plan method
    def mock_recommend_treatment_plan(claim_id, medical_analysis):
        return {
            "claim_id": claim_id,
            "recommendation_timestamp": datetime.datetime.now().isoformat(),
            "recommended_treatments": ["Physical therapy", "Medication"],
            "estimated_duration": "6 weeks"
        }
    
    # Apply the monkeypatches
    monkeypatch.setattr(medical_agent, "analyze_medical_records", mock_analyze_medical_records)
    monkeypatch.setattr(medical_agent, "assess_work_restrictions", mock_assess_work_restrictions)
    monkeypatch.setattr(medical_agent, "recommend_treatment_plan", mock_recommend_treatment_plan)
    
    # Create a test state
    state = {
        "claim_id": "test-claim-123",
        "status": "medical_review",
        "medical_records": [
            {
                "provider_name": "Dr. Test",
                "diagnosis": "Lumbar strain",
                "treatment_plan": "Conservative care"
            }
        ],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Process the state
    updated_state = medical_agent.process(state)
    
    # Assert the state has been updated correctly
    assert "medical_assessment" in updated_state
    assert "diagnosis" in updated_state["medical_assessment"]
    assert "work_restrictions" in updated_state["medical_assessment"]
    assert "treatment_plan" in updated_state["medical_assessment"]
    assert "work_restrictions" in updated_state
    assert "treatment_plan" in updated_state
    assert updated_state["status"] == "compliance_check"
    assert updated_state["current_agent"] == "MedicalAgent"
