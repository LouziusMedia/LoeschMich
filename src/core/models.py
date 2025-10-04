"""Data models using Pydantic"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RequestType(str, Enum):
    """Type of GDPR request"""

    DELETION = "deletion"  # Art. 17 DSGVO
    ACCESS = "access"  # Art. 15 DSGVO
    RECTIFICATION = "rectification"  # Art. 16 DSGVO
    OBJECTION = "objection"  # Art. 21 DSGVO


class RequestStatus(str, Enum):
    """Status of a GDPR request"""

    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    COMPLETED = "completed"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    FAILED = "failed"


class Company(BaseModel):
    """Company/organization model"""

    id: Optional[int] = None
    name: str
    email: EmailStr
    website: Optional[str] = None
    data_protection_officer: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Beispiel GmbH",
                "email": "datenschutz@beispiel.de",
                "website": "https://www.beispiel.de",
                "address": "Musterstraße 1, 12345 Berlin",
            }
        }


class GDPRRequest(BaseModel):
    """GDPR request model"""

    id: Optional[int] = None
    company_id: int
    company_name: str
    request_type: RequestType
    status: RequestStatus = RequestStatus.DRAFT
    subject: str
    body: str
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_data: Optional[dict] = None
    reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    sent_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    reminder_count: int = 0
    last_reminder_at: Optional[datetime] = None
    response_text: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "company_id": 1,
                "company_name": "Beispiel GmbH",
                "request_type": "deletion",
                "subject": "DSGVO Löschantrag gemäß Art. 17 DSGVO",
                "body": "Sehr geehrte Damen und Herren...",
                "user_name": "Max Mustermann",
                "user_email": "max@example.com",
            }
        }


class EmailTemplate(BaseModel):
    """Email template model"""

    name: str
    language: str
    subject: str
    body: str
    variables: list[str] = []

    class Config:
        json_schema_extra = {
            "example": {
                "name": "deletion_request",
                "language": "de",
                "subject": "DSGVO Löschantrag gemäß Art. 17 DSGVO",
                "body": "Sehr geehrte Damen und Herren...",
                "variables": ["company_name", "user_name", "date"],
            }
        }


class WorkflowTask(BaseModel):
    """Workflow task model"""

    id: Optional[int] = None
    request_id: int
    task_type: str  # e.g., "send_email", "check_response", "send_reminder"
    scheduled_at: datetime
    executed_at: Optional[datetime] = None
    status: str = "pending"  # pending, completed, failed
    result: Optional[str] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "request_id": 1,
                "task_type": "send_reminder",
                "scheduled_at": "2025-10-18T10:00:00",
                "status": "pending",
            }
        }
