"""Tests for AI modules"""

from unittest.mock import Mock, patch

import pytest

from src.ai.ollama_client import OllamaClient
from src.ai.request_generator import RequestGenerator
from src.ai.response_analyzer import ResponseAnalyzer, ResponseType
from src.core.models import Company


@pytest.fixture
def mock_ollama():
    """Mock Ollama client"""
    with patch("src.ai.ollama_client.requests") as mock_requests:
        yield mock_requests


def test_ollama_is_available(mock_ollama):
    """Test Ollama availability check"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_ollama.get.return_value = mock_response

    client = OllamaClient()
    assert client.is_available() is True


def test_ollama_generate(mock_ollama):
    """Test Ollama text generation"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Generated text"}
    mock_ollama.post.return_value = mock_response

    client = OllamaClient()
    result = client.generate("Test prompt")

    assert result == "Generated text"
    assert mock_ollama.post.called


def test_request_generator_without_ai():
    """Test request generation without AI"""
    generator = RequestGenerator(use_ai=False)

    company = Company(id=1, name="Test Company", email="test@example.com")

    subject, body = generator.generate_deletion_request(
        company=company,
        user_name="Max Mustermann",
        user_email="max@example.com",
        reason="Test reason",
    )

    assert "DSGVO" in subject or "GDPR" in subject
    assert "Test Company" in body
    assert "Max Mustermann" in body
    assert "Test reason" in body


def test_request_generator_reminder():
    """Test reminder generation"""
    from datetime import datetime

    generator = RequestGenerator(use_ai=False)

    company = Company(id=1, name="Test Company", email="test@example.com")

    subject, body = generator.generate_reminder(
        company=company, original_date=datetime(2025, 10, 1), user_name="Max Mustermann"
    )

    assert "Erinnerung" in subject or "Reminder" in subject
    assert "01.10.2025" in body


def test_response_analyzer_keyword_completed():
    """Test response analysis - completion"""
    analyzer = ResponseAnalyzer(use_ai=False)

    response_text = "Ihre Daten wurden vollständig gelöscht."
    analysis = analyzer.analyze_response(response_text)

    assert analysis["type"] == ResponseType.COMPLETED
    assert analysis["action_required"] is False


def test_response_analyzer_keyword_acknowledged():
    """Test response analysis - acknowledgment"""
    analyzer = ResponseAnalyzer(use_ai=False)

    response_text = "Wir haben Ihre Anfrage erhalten und werden diese bearbeiten."
    analysis = analyzer.analyze_response(response_text)

    assert analysis["type"] == ResponseType.ACKNOWLEDGED
    assert analysis["action_required"] is True


def test_response_analyzer_keyword_rejected():
    """Test response analysis - rejection"""
    analyzer = ResponseAnalyzer(use_ai=False)

    response_text = "Wir können Ihre Anfrage leider nicht erfüllen aufgrund gesetzlicher Aufbewahrungspflichten."
    analysis = analyzer.analyze_response(response_text)

    assert analysis["type"] == ResponseType.REJECTED
    assert analysis["action_required"] is True


def test_response_analyzer_keyword_needs_info():
    """Test response analysis - needs information"""
    analyzer = ResponseAnalyzer(use_ai=False)

    response_text = "Zur Identifizierung benötigen wir weitere Informationen von Ihnen."
    analysis = analyzer.analyze_response(response_text)

    assert analysis["type"] == ResponseType.NEEDS_INFO
    assert analysis["action_required"] is True


def test_response_analyzer_empty():
    """Test response analysis - empty response"""
    analyzer = ResponseAnalyzer(use_ai=False)

    analysis = analyzer.analyze_response("")

    assert analysis["type"] == ResponseType.UNKNOWN
    assert analysis["action_required"] is True
