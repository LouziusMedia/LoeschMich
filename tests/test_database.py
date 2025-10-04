"""Tests for database operations"""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from src.core.database import Database
from src.core.models import (
    Company,
    GDPRRequest,
    RequestStatus,
    RequestType,
    WorkflowTask,
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = Database(db_path)
    yield db

    # Cleanup
    db_path.unlink(missing_ok=True)


def test_add_company(temp_db):
    """Test adding a company"""
    company = Company(name="Test Company", email="test@example.com", website="https://test.com")

    company_id = temp_db.add_company(company)
    assert company_id > 0

    # Retrieve and verify
    retrieved = temp_db.get_company(company_id)
    assert retrieved is not None
    assert retrieved.name == "Test Company"
    assert retrieved.email == "test@example.com"


def test_get_company_by_name(temp_db):
    """Test retrieving company by name"""
    company = Company(name="Unique Company", email="unique@example.com")

    temp_db.add_company(company)

    retrieved = temp_db.get_company_by_name("Unique Company")
    assert retrieved is not None
    assert retrieved.email == "unique@example.com"


def test_list_companies(temp_db):
    """Test listing all companies"""
    companies = [
        Company(name="Company A", email="a@example.com"),
        Company(name="Company B", email="b@example.com"),
        Company(name="Company C", email="c@example.com"),
    ]

    for company in companies:
        temp_db.add_company(company)

    all_companies = temp_db.list_companies()
    assert len(all_companies) == 3
    assert all_companies[0].name == "Company A"  # Sorted by name


def test_add_request(temp_db):
    """Test adding a GDPR request"""
    # Add company first
    company = Company(name="Test Co", email="test@example.com")
    company_id = temp_db.add_company(company)

    # Add request
    request = GDPRRequest(
        company_id=company_id,
        company_name="Test Co",
        request_type=RequestType.DELETION,
        status=RequestStatus.DRAFT,
        subject="Test Subject",
        body="Test Body",
        user_name="Test User",
    )

    request_id = temp_db.add_request(request)
    assert request_id > 0

    # Retrieve and verify
    retrieved = temp_db.get_request(request_id)
    assert retrieved is not None
    assert retrieved.company_name == "Test Co"
    assert retrieved.request_type == RequestType.DELETION
    assert retrieved.status == RequestStatus.DRAFT


def test_update_request_status(temp_db):
    """Test updating request status"""
    company = Company(name="Test Co", email="test@example.com")
    company_id = temp_db.add_company(company)

    request = GDPRRequest(
        company_id=company_id,
        company_name="Test Co",
        request_type=RequestType.DELETION,
        status=RequestStatus.DRAFT,
        subject="Test",
        body="Test",
    )

    request_id = temp_db.add_request(request)

    # Update status
    temp_db.update_request_status(request_id, RequestStatus.SENT, "Sent successfully")

    # Verify
    updated = temp_db.get_request(request_id)
    assert updated.status == RequestStatus.SENT
    assert updated.sent_at is not None
    assert "Sent successfully" in updated.notes


def test_list_requests_by_status(temp_db):
    """Test filtering requests by status"""
    company = Company(name="Test Co", email="test@example.com")
    company_id = temp_db.add_company(company)

    # Add multiple requests with different statuses
    for i, status in enumerate([RequestStatus.DRAFT, RequestStatus.SENT, RequestStatus.COMPLETED]):
        request = GDPRRequest(
            company_id=company_id,
            company_name="Test Co",
            request_type=RequestType.DELETION,
            status=status,
            subject=f"Test {i}",
            body=f"Body {i}",
        )
        temp_db.add_request(request)

    # Filter by status
    sent_requests = temp_db.list_requests(RequestStatus.SENT)
    assert len(sent_requests) == 1
    assert sent_requests[0].status == RequestStatus.SENT


def test_add_workflow_task(temp_db):
    """Test adding workflow tasks"""
    company = Company(name="Test Co", email="test@example.com")
    company_id = temp_db.add_company(company)

    request = GDPRRequest(
        company_id=company_id,
        company_name="Test Co",
        request_type=RequestType.DELETION,
        status=RequestStatus.SENT,
        subject="Test",
        body="Test",
    )
    request_id = temp_db.add_request(request)

    # Add task
    task = WorkflowTask(
        request_id=request_id,
        task_type="send_reminder",
        scheduled_at=datetime.now(),
        status="pending",
    )

    task_id = temp_db.add_task(task)
    assert task_id > 0


def test_get_pending_tasks(temp_db):
    """Test retrieving pending tasks"""
    company = Company(name="Test Co", email="test@example.com")
    company_id = temp_db.add_company(company)

    request = GDPRRequest(
        company_id=company_id,
        company_name="Test Co",
        request_type=RequestType.DELETION,
        status=RequestStatus.SENT,
        subject="Test",
        body="Test",
    )
    request_id = temp_db.add_request(request)

    # Add pending task
    task = WorkflowTask(
        request_id=request_id,
        task_type="send_reminder",
        scheduled_at=datetime.now(),
        status="pending",
    )
    temp_db.add_task(task)

    # Retrieve pending tasks
    pending = temp_db.get_pending_tasks()
    assert len(pending) >= 1
    assert pending[0].status == "pending"
