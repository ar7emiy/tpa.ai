# database/sqlite/models.py
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Claim(Base):
    __tablename__ = 'claims'
    
    claim_id = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    claimant = relationship("Claimant", back_populates="claim", uselist=False)
    employer = relationship("Employer", back_populates="claim", uselist=False)
    injury = relationship("Injury", back_populates="claim", uselist=False)
    medical_records = relationship("MedicalRecord", back_populates="claim")
    verification = relationship("Verification", back_populates="claim", uselist=False)
    compliance = relationship("Compliance", back_populates="claim", uselist=False)
    decision = relationship("Decision", back_populates="claim", uselist=False)
    payment = relationship("Payment", back_populates="claim", uselist=False)
    conversations = relationship("Conversation", back_populates="claim")

class Claimant(Base):
    __tablename__ = 'claimants'
    
    claimant_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    name = Column(String, nullable=False)
    contact_info = Column(Text)
    employment_date = Column(DateTime)
    
    # Relationships
    claim = relationship("Claim", back_populates="claimant")

class Employer(Base):
    __tablename__ = 'employers'
    
    employer_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    company_name = Column(String, nullable=False)
    contact_info = Column(Text)
    
    # Relationships
    claim = relationship("Claim", back_populates="employer")

class Injury(Base):
    __tablename__ = 'injuries'
    
    injury_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    date = Column(DateTime)
    location = Column(String)
    description = Column(Text)
    cause = Column(Text)
    
    # Relationships
    claim = relationship("Claim", back_populates="injury")
    witnesses = relationship("Witness", back_populates="injury")

class Witness(Base):
    __tablename__ = 'witnesses'
    
    witness_id = Column(String, primary_key=True)
    injury_id = Column(String, ForeignKey('injuries.injury_id'))
    name = Column(String)
    contact_info = Column(Text)
    statement = Column(Text)
    
    # Relationships
    injury = relationship("Injury", back_populates="witnesses")

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    
    record_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    provider_name = Column(String)
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    restrictions = Column(Text)
    date = Column(DateTime)
    
    # Relationships
    claim = relationship("Claim", back_populates="medical_records")

class Verification(Base):
    __tablename__ = 'verifications'
    
    verification_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    employment_verified = Column(Boolean, default=False)
    policy_valid = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    notes = Column(Text)
    
    # Relationships
    claim = relationship("Claim", back_populates="verification")

class Compliance(Base):
    __tablename__ = 'compliance'
    
    compliance_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    documentation_complete = Column(Boolean, default=False)
    timely_filing = Column(Boolean, default=False)
    compliance_date = Column(DateTime)
    notes = Column(Text)
    
    # Relationships
    claim = relationship("Claim", back_populates="compliance")

class Decision(Base):
    __tablename__ = 'decisions'
    
    decision_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    approved = Column(Boolean)
    decision_date = Column(DateTime)
    reasoning = Column(Text)
    
    # Relationships
    claim = relationship("Claim", back_populates="decision")

class Payment(Base):
    __tablename__ = 'payments'
    
    payment_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    amount = Column(Integer)
    payment_date = Column(DateTime)
    payment_type = Column(String)
    
    # Relationships
    claim = relationship("Claim", back_populates="payment")

class Conversation(Base):
    __tablename__ = 'conversations'
    
    conversation_id = Column(String, primary_key=True)
    claim_id = Column(String, ForeignKey('claims.claim_id'))
    stakeholder_type = Column(String)  # claimant, employer, medical_provider
    conversation_date = Column(DateTime)
    conversation_text = Column(Text)
    
    # Relationships
    claim = relationship("Claim", back_populates="conversations")
