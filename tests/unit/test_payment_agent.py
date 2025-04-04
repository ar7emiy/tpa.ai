# tests/unit/test_payment_agent.py
import pytest
import json
import datetime
from agents.payment_agent import PaymentAgent

@pytest.fixture
def payment_agent():
    """Create a payment agent for testing."""
    return PaymentAgent()

def test_agent_initialization(payment_agent):
    """Test that the agent initializes correctly."""
    assert payment_agent.agent_name == "PaymentAgent"
    assert "Payment Agent" in payment_agent.system_prompt
    assert "Process payments for approved claims" in payment_agent.system_prompt

def test_handle_function_call_process_payment(payment_agent):
    """Test handling of payment processing."""
    state = {}
    function_name = "process_payment"
    function_args = {
        "payment_amount": 800.00,
        "payment_type": "initial",
        "payment_date": datetime.datetime.now().isoformat(),
        "payment_period": "First week of disability",
        "payment_method": "Direct deposit",
        "notes": "Initial payment for approved claim"
    }
    
    response, updated_state = payment_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "payment_status" in updated_state
    assert "payments" in updated_state["payment_status"]
    assert updated_state["payment_status"]["payments"][0] == function_args
    assert "last_payment_date" in updated_state["payment_status"]
    assert updated_state["payment_status"]["payment_processed"] == True

def test_handle_function_call_schedule_future_payments(payment_agent):
    """Test handling of payment scheduling."""
    state = {}
    function_name = "schedule_future_payments"
    function_args = {
        "payment_schedule": [
            {
                "scheduled_date": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat(),
                "estimated_amount": 800.00,
                "payment_type": "weekly"
            },
            {
                "scheduled_date": (datetime.datetime.now() + datetime.timedelta(days=14)).isoformat(),
                "estimated_amount": 800.00,
                "payment_type": "weekly"
            }
        ],
        "payment_frequency": "weekly",
        "next_review_date": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
    }
    
    response, updated_state = payment_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "payment_status" in updated_state
    assert "payment_schedule" in updated_state["payment_status"]
    assert updated_state["payment_status"]["payment_frequency"] == "weekly"
    assert "next_review_date" in updated_state["payment_status"]

def test_handle_function_call_track_recovery(payment_agent):
    """Test handling of recovery tracking."""
    state = {}
    function_name = "track_recovery"
    function_args = {
        "recovery_status": "improving",
        "work_status": "light duty",
        "fully_recovered": False,
        "recovery_date": "",
        "continuing_treatment": True,
        "next_medical_review": (datetime.datetime.now() + datetime.timedelta(days=14)).isoformat(),
        "notes": "Patient showing good improvement with physical therapy"
    }
    
    response, updated_state = payment_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "recovery_status" in updated_state
    assert updated_state["recovery_status"]["recovery_status"] == "improving"
    assert updated_state["recovery_status"]["work_status"] == "light duty"
    assert updated_state["recovery_status"]["fully_recovered"] == False
    assert "assessment_date" in updated_state["recovery_status"]

def test_process_approved_claim(payment_agent, monkeypatch):
    """Test processing a newly approved claim."""
    # Mock the process_initial_payment method
    def mock_process_initial_payment(claim_id, decision_status):
        return {
            "claim_id": claim_id,
            "processing_timestamp": datetime.datetime.now().isoformat(),
            "payment_amount": 800.00,
            "payment_type": "initial",
            "payment_date": datetime.datetime.now().isoformat(),
            "payment_period": "First week of disability"
        }
    
    # Mock the schedule_payments method
    def mock_schedule_payments(claim_id, decision_status):
        return {
            "claim_id": claim_id,
            "scheduling_timestamp": datetime.datetime.now().isoformat(),
            "payment_schedule": [
                {
                    "scheduled_date": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat(),
                    "estimated_amount": 800.00,
                    "payment_type": "weekly"
                }
            ],
            "payment_frequency": "weekly",
            "next_review_date": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
        }
    
    # Apply the monkeypatches
    monkeypatch.setattr(payment_agent, "process_initial_payment", mock_process_initial_payment)
    monkeypatch.setattr(payment_agent, "schedule_payments", mock_schedule_payments)
    
    # Create a test state for a newly approved claim
    state = {
        "claim_id": "test-claim-123",
        "status": "approved",
        "decision_status": {
            "approved": True,
            "weekly_amount": 800.00,
            "decision_date": datetime.datetime.now().isoformat()
        },
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Process the state
    updated_state = payment_agent.process(state)
    
    # Assert the state has been updated correctly
    assert "payment_status" in updated_state
    assert "payments" in updated_state["payment_status"]
    assert len(updated_state["payment_status"]["payments"]) == 1
    assert updated_state["payment_status"]["payment_processed"] == True
    assert "payment_schedule" in updated_state["payment_status"]
    assert "payment_frequency" in updated_state["payment_status"]
    assert updated_state["status"] == "payment_processing"
    assert updated_state["current_agent"] == "PaymentAgent"

def test_process_recovery_check(payment_agent, monkeypatch):
    """Test processing a claim in recovery check status."""
    # Mock the assess_recovery method
    def mock_assess_recovery(claim_id, claim_data):
        return {
            "claim_id": claim_id,
            "assessment_timestamp": datetime.datetime.now().isoformat(),
            "recovery_status": "fully recovered",
            "work_status": "full duty",
            "fully_recovered": True,
            "recovery_date": datetime.datetime.now().isoformat(),
            "continuing_treatment": False,
            "next_medical_review": "",
            "notes": "Patient has fully recovered and returned to full duty"
        }
    
    # Apply the monkeypatch
    monkeypatch.setattr(payment_agent, "assess_recovery", mock_assess_recovery)
    
    # Create a test state for a claim in recovery check
    state = {
        "claim_id": "test-claim-123",
        "status": "recovery_check",
        "decision_status": {
            "approved": True,
            "weekly_amount": 800.00
        },
        "payment_status": {
            "payments": [
                {
                    "payment_amount": 800.00,
                    "payment_type": "initial",
                    "payment_date": (datetime.datetime.now() - datetime.timedelta(days=14)).isoformat()
                }
            ],
            "payment_processed": True
        },
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Process the state
    updated_state = payment_agent.process(state)
    
    # Assert the state has been updated correctly
    assert "recovery_status" in updated_state
    assert updated_state["recovery_status"]["fully_recovered"] == True
    assert len(updated_state["payment_status"]["payments"]) == 2
    assert updated_state["payment_status"]["payments"][-1]["payment_type"] == "final"
    assert updated_state["status"] == "closed"
