"""Tests for email functionality"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from src.communication.email_sender import EmailSender


@pytest.fixture
def mock_smtp():
    """Mock SMTP server"""
    with patch("src.communication.email_sender.smtplib.SMTP") as mock:
        smtp_instance = MagicMock()
        mock.return_value.__enter__.return_value = smtp_instance
        yield smtp_instance


@pytest.fixture
def email_sender():
    """Create email sender with test config"""
    with patch("src.communication.email_sender.Config") as mock_config:
        mock_config.SMTP_SERVER = "smtp.test.com"
        mock_config.SMTP_PORT = 587
        mock_config.SMTP_USERNAME = "test@example.com"
        mock_config.SMTP_PASSWORD = "password"
        mock_config.SENDER_EMAIL = "test@example.com"
        mock_config.SENDER_NAME = "Test Sender"

        sender = EmailSender()
        return sender


def test_validate_config(email_sender):
    """Test configuration validation"""
    assert email_sender.validate_config() is True


def test_send_email_success(email_sender, mock_smtp):
    """Test successful email sending"""
    result = email_sender.send_email(
        to_email="recipient@example.com", subject="Test Subject", body="Test Body"
    )

    assert result is True
    assert mock_smtp.starttls.called
    assert mock_smtp.login.called
    assert mock_smtp.send_message.called


def test_send_email_with_cc_bcc(email_sender, mock_smtp):
    """Test email with CC and BCC"""
    result = email_sender.send_email(
        to_email="recipient@example.com",
        subject="Test Subject",
        body="Test Body",
        cc=["cc@example.com"],
        bcc=["bcc@example.com"],
    )

    assert result is True
    assert mock_smtp.send_message.called


def test_send_email_html(email_sender, mock_smtp):
    """Test HTML email"""
    result = email_sender.send_email(
        to_email="recipient@example.com",
        subject="Test Subject",
        body="<h1>Test HTML</h1>",
        html=True,
    )

    assert result is True


def test_test_connection_success(email_sender, mock_smtp):
    """Test SMTP connection test"""
    result = email_sender.test_connection()
    assert result is True
    assert mock_smtp.starttls.called
    assert mock_smtp.login.called
