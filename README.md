aiTPA: AI-Powered Workers' Compensation Claims Processing System
Overview
aiTPA is an advanced multi-agent system designed to automate and streamline workers' compensation claims processing. Leveraging large language models and a sophisticated workflow orchestration system, aiTPA creates a closed-loop simulation where AI agents play the roles of various stakeholders in the claims process.
The system handles the entire claims lifecycle - from initial reporting through final resolution - using specialized AI agents to perform different functions in the claims process.
Features

Multi-Agent Architecture: Specialized agents handle different aspects of claims processing
Conversation Simulation: Realistic stakeholder conversations to gather claim information
Automated Decision Making: AI-powered claim verification, assessment, and decisions
Structured Data Extraction: Convert natural language into structured data
Workflow Automation: Complete end-to-end claims process management
Vector Search: Semantic search capabilities for claim documentation

System Architecture
Components

Agent System: Specialized AI agents for different aspects of claims processing
Workflow Engine: LangGraph-based state machine for process orchestration
Database Layer: Structured (SQLite) and vector (ChromaDB) storage
Function Calling: Gemini API integration for tool use

Agents

Conversational Agent

Simulates conversations with stakeholders (claimant, employer, medical providers)
Extracts structured information from natural language
Handles initial claim intake and follow-up questions


Verification Agent

Validates employment status and eligibility
Confirms insurance policy details
Determines if claim meets basic requirements


Medical Assessment Agent

Reviews medical documentation
Evaluates treatment plans and recovery timelines
Assesses work restrictions


Compliance Agent

Ensures all documentation requirements are met
Verifies reporting timelines
Checks regulatory compliance


Decision Agent

Evaluates all evidence
Determines claim approval/denial
Calculates compensation amounts


Payment Agent

Processes payment for approved claims
Calculates benefit amounts
Tracks payment history


Coordinator Agent

Orchestrates the overall workflow
Assigns tasks to appropriate agents
Tracks claim progress



Workflow
The system implements a state machine workflow with the following key states:

NEW → VERIFICATION → MEDICAL_REVIEW → COMPLIANCE_CHECK → DECISION_PENDING → APPROVED/DENIED → PAYMENT_PROCESSING → RECOVERY_CHECK → CLOSED

Installation
Prerequisites

Python 3.10+
SQLite
ChromaDB
Google API key for Gemini models
