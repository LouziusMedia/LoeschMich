"""Tests for workflow orchestration"""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.core.database import Database
from src.core.models import Company, RequestStatus
from src.workflow.orchestrator import WorkflowOrchestrator


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = Database(db_path)
    yield db

    # Cleanup
    db_path.unlink(missing_ok=True)


@pytest.fixture
def orchestrator(temp_db):
    """Create orchestrator with mocked email sender"""
    with patch("src.workflow.orchestrator.EmailSender") as mock_sender:
        mock_sender_instance = Mock()
        mock_sender_instance.send_email.return_value = True
        mock_sender.return_value = mock_sender_instance

        orch = WorkflowOrchestrator(temp_db)
        orch.email_sender = mock_sender_instance

        yield orch


def test_create_request(orchestrator, temp_db):
    """Test creating a GDPR request"""
    company = Company(name="Test Company", email="test@example.com")
    company_id = temp_db.add_company(company)
    company.id = company_id

    request_id = orchestrator.create_and_send_request(
        company=company,
        user_name="Test User",
        user_email="user@example.com",
        reason="Test reason",
        auto_send=False,
    )

    assert request_id is not None

    # Verify request was created
    request = temp_db.get_request(request_id)
    assert request is not None
    assert request.company_name == "Test Company"
    assert request.user_name == "Test User"
    assert request.status == RequestStatus.DRAFT


def test_send_request(orchestrator, temp_db):
    """Test sending a request"""
    company = Company(name="Test Company", email="test@example.com")
    company_id = temp_db.add_company(company)
    company.id = company_id

    request_id = orchestrator.create_and_send_request(
        company=company, user_name="Test User", auto_send=False
    )

    # Send the request
    result = orchestrator.send_request(request_id)
    assert result is True

    # Verify status updated
    request = temp_db.get_request(request_id)
    assert request.status == RequestStatus.SENT
    assert request.sent_at is not None

    # Verify email was sent
    assert orchestrator.email_sender.send_email.called


def test_send_reminder(orchestrator, temp_db):
    """Test sending a reminder"""
    company = Company(name="Test Company", email="test@example.com")
    company_id = temp_db.add_company(company)
    company.id = company_id

    request_id = orchestrator.create_and_send_request(
        company=company, user_name="Test User", auto_send=True
    )

    # Send reminder
    result = orchestrator.send_reminder(request_id)
    assert result is True

    # Verify reminder count increased
    request = temp_db.get_request(request_id)
    assert request.reminder_count == 1


def test_process_response(orchestrator, temp_db):
    """Test processing a company response"""
    company = Company(name="Test Company", email="test@example.com")
    company_id = temp_db.add_company(company)
    company.id = company_id

    request_id = orchestrator.create_and_send_request(
        company=company, user_name="Test User", auto_send=True
    )

    # Process response
    response_text = "Ihre Daten wurden vollständig gelöscht."
    analysis = orchestrator.process_response(request_id, response_text)

    assert analysis is not None
    assert "type" in analysis

    # Verify request status updated
    request = temp_db.get_request(request_id)
    assert request.status == RequestStatus.COMPLETED


def test_execute_pending_tasks(orchestrator, temp_db):
    """Test executing pending workflow tasks"""
    company = Company(name="Test Company", email="test@example.com")
    company_id = temp_db.add_company(company)
    company.id = company_id

    # Create and send request (this schedules tasks)
    request_id = orchestrator.create_and_send_request(
        company=company, user_name="Test User", auto_send=True
    )

    # Get pending tasks
    tasks = temp_db.get_pending_tasks(datetime(2099, 12, 31))
    assert len(tasks) > 0
