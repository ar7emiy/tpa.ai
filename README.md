# aiTPA: AI-Powered Workers' Compensation Claims Processing System

## Overview

aiTPA is an advanced multi-agent system designed to automate and streamline workers' compensation claims processing. Leveraging large language models and a sophisticated workflow orchestration system, aiTPA creates a closed-loop simulation where AI agents play the roles of various stakeholders in the claims process.

The system handles the entire claims lifecycle - from initial reporting through final resolution - using specialized AI agents to perform different functions in the claims process.

## Features

- **Multi-Agent Architecture**: Specialized agents handle different aspects of claims processing
- **Conversation Simulation**: Realistic stakeholder conversations to gather claim information
- **Automated Decision Making**: AI-powered claim verification, assessment, and decisions
- **Structured Data Extraction**: Convert natural language into structured data
- **Workflow Automation**: Complete end-to-end claims process management
- **Vector Search**: Semantic search capabilities for claim documentation

## System Architecture

### Components

- **Agent System**: Specialized AI agents for different aspects of claims processing
- **Workflow Engine**: LangGraph-based state machine for process orchestration
- **Database Layer**: Structured (SQLite) and vector (ChromaDB) storage
- **Function Calling**: Gemini API integration for tool use

### Agents

1. **Conversational Agent**
   - Simulates conversations with stakeholders (claimant, employer, medical providers)
   - Extracts structured information from natural language
   - Handles initial claim intake and follow-up questions

2. **Verification Agent**
   - Validates employment status and eligibility
   - Confirms insurance policy details
   - Determines if claim meets basic requirements

3. **Medical Assessment Agent**
   - Reviews medical documentation
   - Evaluates treatment plans and recovery timelines
   - Assesses work restrictions

4. **Compliance Agent**
   - Ensures all documentation requirements are met
   - Verifies reporting timelines
   - Checks regulatory compliance

5. **Decision Agent**
   - Evaluates all evidence
   - Determines claim approval/denial
   - Calculates compensation amounts

6. **Payment Agent**
   - Processes payment for approved claims
   - Calculates benefit amounts
   - Tracks payment history

7. **Coordinator Agent**
   - Orchestrates the overall workflow
   - Assigns tasks to appropriate agents
   - Tracks claim progress

### Workflow

The system implements a state machine workflow with the following key states:
- NEW → VERIFICATION → MEDICAL_REVIEW → COMPLIANCE_CHECK → DECISION_PENDING → APPROVED/DENIED → PAYMENT_PROCESSING → RECOVERY_CHECK → CLOSED

## Installation

### Prerequisites

- Python 3.10+
- SQLite
- ChromaDB
- Google API key for Gemini models

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/aiTPA.git
   cd aiTPA
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

5. Initialize databases:
   ```bash
   python -m scripts.init_db
   ```

## Usage

### Processing a New Claim

```bash
python app.py --claim-file path/to/claim.json --output-file results.json
```

### Using the Test Suite

```bash
pytest
```

### Development Server

```bash
python app.py --dev-mode
```

## Technology Stack

- **Python 3.10+**: Primary programming language
- **LangGraph**: For state management and agent orchestration
- **Google Generative AI SDK (Gemini)**: For LLM capabilities with function calling
- **SQLite**: For structured data storage
- **ChromaDB**: For vector embeddings and semantic search
- **Pytest**: For comprehensive testing

## Project Structure

```
aiTPA/
├── README.md                 # Project overview and setup instructions
├── requirements.txt          # Project dependencies
├── config/                   # Configuration files
├── database/                 # Database modules
│   ├── sqlite/               # Structured data storage
│   └── vector/               # Vector database
├── agents/                   # Agent implementations
├── workflow/                 # Workflow definition
├── tools/                    # Function calling tools
├── prompts/                  # Prompt templates
├── utils/                    # Utility functions
├── tests/                    # Tests
└── app.py                    # Main application entry point
```

## Development Status

This project is currently in active development. The following components are implemented:

- [x] Core agent architecture
- [x] Database schemas
- [x] Workflow engine
- [x] Conversational agent
- [x] Verification agent
- [ ] Medical assessment agent
- [ ] Compliance agent
- [ ] Decision agent
- [ ] Payment agent
- [ ] Recovery agent
- [ ] End-to-end testing
- [ ] Production deployment

## Acknowledgements

- Google for providing the Gemini API
- LangChain/LangGraph team for the workflow orchestration framework
- ChromaDB for vector storage capabilities
