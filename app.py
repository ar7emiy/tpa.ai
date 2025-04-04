# app.py
import argparse
import json
import datetime
import uuid
from config.settings import SETTINGS
from database.sqlite.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.vector.operations import init_chromadb
from workflow.graph import create_workflow
from workflow.states import ClaimState, ClaimStatus

def initialize_database():
    """Initialize the SQLite database."""
    engine = create_engine("sqlite:///wc_claims.db")
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    return session

def initialize_vector_db():
    """Initialize ChromaDB."""
    client = init_chromadb()
    return client

def create_initial_state(claim_details=None):
    """Create initial state for a new claim."""
    claim_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    initial_state = ClaimState(
        claim_id=claim_id,
        status=ClaimStatus.NEW,
        claimant_info={},
        employer_info={},
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
    
    # If claim details provided, update initial state
    if claim_details:
        for key, value in claim_details.items():
            if key in initial_state:
                initial_state[key] = value
    
    return initial_state

def process_claim(initial_state):
    """Process a claim through the workflow."""
    # Create workflow
    workflow = create_workflow()
    
    # Process claim
    result = workflow.invoke(initial_state)
    
    return result

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="Workers' Compensation Claims Processing System")
    parser.add_argument("--claim-file", help="JSON file with initial claim details")
    parser.add_argument("--output-file", help="Output file for processed claim")
    args = parser.parse_args()
    
    # Initialize databases
    session = initialize_database()
    vector_client = initialize_vector_db()
    
    # Create initial state
    claim_details = None
    if args.claim_file:
        with open(args.claim_file, 'r') as f:
            claim_details = json.load(f)
    
    initial_state = create_initial_state(claim_details)
    
    # Process claim
    result = process_claim(initial_state)
    
    # Output result
    if args.output_file:
        with open(args.output_file, 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))
    
    print(f"Claim processing complete. Final status: {result['status']}")

if __name__ == "__main__":
    main()
