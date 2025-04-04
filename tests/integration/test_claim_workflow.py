# tests/integration/test_claim_workflow.py
import pytest
import json
import datetime
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.sqlite.models import Base
from database.vector.operations import init_chromadb
from workflow.graph import create_workflow
from workflow.states import ClaimState, ClaimStatus

@pytest.fixture
def setup_database():
    """Set up test database."""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Cleanup
    session.close()

@pytest.fixture
def setup_vector_db():
    """Set up test vector database."""
    # Use in-memory ChromaDB for testing
    client = chromadb.Client()
    
    return client

@pytest.fixture
def workflow():
    """Create workflow for testing."""
    return create_workflow()

@pytest.fixture
def sample_claim_state():
    """Create a sample claim state for testing."""
    claim_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    return ClaimState(
        claim_id=claim_id,
        status=ClaimStatus.NEW,
        claimant_info={
            "name": "John Doe",
            "contact_info": "john@example.com",
            "injury_date": "2025-03-01T00:00:00Z",
            "injury_location": "Warehouse loading dock",
            "injury_description": "Back strain",
            "how_it_occurred": "Lifting heavy box",
            "witnesses": ["Jane Smith"],
            "medical_attention": True,
            "medical_provider": "City General Hospital"
        },
        employer_info={
            "company_name": "Acme Corp",
            "supervisor_name": "Jane Manager",
            "contact_info": "jane@acme.com",
            "employment_duration": "3 years",
            "job_title": "Warehouse Associate",
            "incident_reported": True,
            "report_date": "2025-03-01T14:30:00Z"
        },
        injury_details={},
        witness_info=[],
        medical_records=[],
        treatment_plan={},
        work_restrictions={},
        verification_status={},
        compliance_status={},
        decision_status={},
        payment_status={},
        recovery_status={},
        conversations={},
        created_at=timestamp,
        updated_at=timestamp,
        current_agent="coordinator"
    )

def test_end_to_end_claim_processing(setup_database, setup_vector_db, workflow, sample_claim_state, monkeypatch):
    """Test end-to-end claim processing through the workflow."""
    # Mock agent processing functions to return predictable results
    def mock_conversational_process(state):
        state["conversations"] = {
            "claimant": [{
                "conversation_text": "Simulated claimant conversation",
                "extracted_data": state["claimant_info"],
                "stakeholder_type": "claimant",
                "timestamp": datetime.datetime.now().isoformat()
            }],
            "employer": [{
                "conversation_text": "Simulated employer conversation",
                "extracted_data": state["employer_info"],
                "stakeholder_type": "employer",
                "timestamp": datetime.datetime.now().isoformat()
            }]
        }
        state["status"] = ClaimStatus.VERIFICATION
        return state
    
    def mock_verification_process(state):
        state["verification_status"] = {
            "employment_verified": True,
            "eligible_for_benefits": True,
            "verification_timestamp": datetime.datetime.now().isoformat(),
            "verification_method": "Test verification",
            "verification_notes": "Verified for testing"
        }
        state["status"] = ClaimStatus.MEDICAL_REVIEW
        return state
    
    def mock_medical_process(state):
        state["medical_records"] = [{
            "provider_name": "Dr. Smith",
            "facility": "City General Hospital",
            "diagnosis": "Lumbar strain",
            "treatment_plan": "Physical therapy, rest, NSAIDs",
            "work_restrictions": "No lifting over 15 lbs for 2 weeks",
            "estimated_recovery": "3-4 weeks",
            "follow_up_date": (datetime.datetime.now() + datetime.timedelta(days=14)).isoformat()
        }]
        state["status"] = ClaimStatus.COMPLIANCE_CHECK
        return state
    
    def mock_compliance_process(state):
        state["compliance_status"] = {
            "is_compliant": True,
            "documentation_complete": True,
            "timely_filing": True,
            "compliance_timestamp": datetime.datetime.now().isoformat(),
            "compliance_notes": "All requirements met"
        }
        state["status"] = ClaimStatus.DECISION_PENDING
        return state
    
    def mock_decision_process(state):
        state["decision_status"] = {
            "approved": True,
            "decision_date": datetime.datetime.now().isoformat(),
            "reasoning": "Medical evidence supports work-related injury with clear treatment plan"
        }
        state["status"] = ClaimStatus.APPROVED
        return state
    
    def mock_payment_process(state):
        state["payment_status"] = {
            "payment_processed": True,
            "amount": 1200,
            "payment_date": datetime.datetime.now().isoformat(),
            "payment_type": "Temporary disability"
        }
        state["status"] = ClaimStatus.PAYMENT_PROCESSING
        
        # Also handle recovery
        state["recovery_status"] = {
            "fully_recovered": True,
            "recovery_date": (datetime.datetime.now() + datetime.timedelta(days=28)).isoformat(),
            "notes": "Patient has completed physical therapy and is ready to return to full duty"
        }
        state["status"] = ClaimStatus.CLOSED
        return state
    
    # Apply monkeypatches to agent nodes in workflow
    import workflow.graph
    monkeypatch.setattr(workflow.nodes["conversational"].fn, "__call__", mock_conversational_process)
    monkeypatch.setattr(workflow.nodes["verification"].fn, "__call__", mock_verification_process)
    monkeypatch.setattr(workflow.nodes["medical"].fn, "__call__", mock_medical_process)
    monkeypatch.setattr(workflow.nodes["compliance"].fn, "__call__", mock_compliance_process)
    monkeypatch.setattr(workflow.nodes["decision"].fn, "__call__", mock_decision_process)
    monkeypatch.setattr(workflow.nodes["payment"].fn, "__call__", mock_payment_process)
    
    # Process the claim
    result = workflow.invoke(sample_claim_state)
    
    # Assert the claim was processed correctly
    assert result["status"] == ClaimStatus.CLOSED
    assert "verification_status" in result
    assert result["verification_status"]["employment_verified"] is True
    assert "medical_records" in result
    assert "compliance_status" in result
    assert result["compliance_status"]["is_compliant"] is True
    assert "decision_status" in result
    assert result["decision_status"]["approved"] is True
    assert "payment_status" in result
    assert result["payment_status"]["payment_processed"] is True
    assert "recovery_status" in result
    assert result["recovery_status"]["fully_recovered"] is True
