# tests/unit/test_conversational_agent.py
import pytest
import json
import datetime
from agents.conversational_agent import ConversationalAgent

@pytest.fixture
def conversational_agent():
    """Create a conversational agent for testing."""
    return ConversationalAgent()

def test_agent_initialization(conversational_agent):
    """Test that the agent initializes correctly."""
    assert conversational_agent.agent_name == "ConversationalAgent"
    assert "Conversational Agent" in conversational_agent.system_prompt
    assert "Extract relevant information" in conversational_agent.system_prompt.lower()

def test_handle_function_call_claimant_data(conversational_agent):
    """Test handling of claimant data extraction."""
    state = {}
    function_name = "extract_claimant_data"
    function_args = {
        "name": "John Doe",
        "contact_info": "john@example.com",
        "injury_date": "2025-03-01T00:00:00Z",
        "injury_location": "Warehouse loading dock",
        "injury_description": "Back strain",
        "how_it_occurred": "Lifting heavy box",
        "witnesses": ["Jane Smith"],
        "medical_attention": True,
        "medical_provider": "City General Hospital"
    }
    
    response, updated_state = conversational_agent.handle_function_call(
        function_name, function_args, state
    )
    
    assert response is not None
    assert "claimant_info" in updated_state
    assert updated_state["claimant_info"] == function_args

def test_simulate_conversation(conversational_agent, monkeypatch):
    """Test conversation simulation with a stakeholder."""
    # Mock the Gemini model response
    class MockResponse:
        def __init__(self):
            self.text = "Simulated conversation text"
            self.candidates = [MockCandidate()]
    
    class MockCandidate:
        def __init__(self):
            self.content = MockContent()
    
    class MockContent:
        def __init__(self):
            self.parts = [MockPart()]
    
    class MockPart:
        def __init__(self):
            self.function_call = MockFunctionCall()
    
    class MockFunctionCall:
        def __init__(self):
            self.name = "extract_claimant_data"
            self.args = json.dumps({
                "name": "John Doe",
                "contact_info": "john@example.com",
                "injury_date": "2025-03-01T00:00:00Z",
                "injury_description": "Back strain",
                "how_it_occurred": "Lifting heavy box"
            })
    
    # Mock the chat.send_message method
    class MockChat:
        def send_message(self, prompt):
            return MockResponse()
    
    # Mock the model.start_chat method
    def mock_start_chat(*args, **kwargs):
        return MockChat()
    
    # Apply the monkeypatch
    monkeypatch.setattr(conversational_agent.model, "start_chat", mock_start_chat)
    
    # Run the test
    result = conversational_agent.simulate_conversation(
        "claimant",
        {"claim_id": "test-claim-123"},
        "initial claim information"
    )
    
    assert "conversation_text" in result
    assert "extracted_data" in result
    assert "stakeholder_type" in result
    assert "timestamp" in result
    assert result["stakeholder_type"] == "claimant"
    assert result["extracted_data"]["name"] == "John Doe"

def test_process_new_claim(conversational_agent, monkeypatch):
    """Test processing a new claim."""
    # Mock simulate_conversation to return predictable results
    def mock_simulate_conversation(role, context, goal):
        if role == "claimant":
            return {
                "conversation_text": "Simulated claimant conversation",
                "extracted_data": {
                    "name": "John Doe",
                    "injury_date": "2025-03-01T00:00:00Z",
                    "injury_description": "Back strain",
                    "how_it_occurred": "Lifting heavy box"
                },
                "stakeholder_type": "claimant",
                "timestamp": datetime.datetime.now().isoformat()
            }
        elif role == "employer":
            return {
                "conversation_text": "Simulated employer conversation",
                "extracted_data": {
                    "company_name": "Acme Corp",
                    "supervisor_name": "Jane Manager",
                    "incident_reported": True
                },
                "stakeholder_type": "employer",
                "timestamp": datetime.datetime.now().isoformat()
            }
        return {}
    
    # Apply the monkeypatch
    monkeypatch.setattr(conversational_agent, "simulate_conversation", mock_simulate_conversation)
    
    # Create a test state
    state = {
        "claim_id": "test-claim-123",
        "status": "new",
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Process the state
    updated_state = conversational_agent.process(state)
    
    # Assert the state has been updated correctly
    assert "conversations" in updated_state
    assert "claimant" in updated_state["conversations"]
    assert "employer" in updated_state["conversations"]
    assert "claimant_info" in updated_state
    assert "employer_info" in updated_state
    assert updated_state["status"] == "verification"
    assert updated_state["claimant_info"]["name"] == "John Doe"
    assert updated_state["employer_info"]["company_name"] == "Acme Corp"
