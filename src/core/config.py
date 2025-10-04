"""Configuration management using environment variables"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    TEMPLATES_DIR = BASE_DIR / "templates"

    # SMTP Configuration
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    SENDER_NAME: str = os.getenv("SENDER_NAME", "")

    # Ollama Configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")

    # Database Configuration
    DATABASE_PATH: Path = Path(
        os.getenv("DATABASE_PATH", str(DATA_DIR / "gdpr_requests.db"))
    )

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Path = Path(os.getenv("LOG_FILE", str(LOGS_DIR / "gdpr_tool.log")))

    # Security
    ENCRYPTION_KEY: Optional[str] = os.getenv("ENCRYPTION_KEY")

    # Workflow Settings
    AUTO_SEND_ENABLED: bool = os.getenv("AUTO_SEND_ENABLED", "false").lower() == "true"
    RETRY_ATTEMPTS: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
    RETRY_DELAY_DAYS: int = int(os.getenv("RETRY_DELAY_DAYS", "14"))
    ESCALATION_DELAY_DAYS: int = int(os.getenv("ESCALATION_DELAY_DAYS", "30"))

    # Language Settings
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "de")

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.TEMPLATES_DIR.mkdir(exist_ok=True)
        (cls.DATA_DIR / "requests").mkdir(exist_ok=True)
        (cls.DATA_DIR / "responses").mkdir(exist_ok=True)
        (cls.DATA_DIR / "tracking").mkdir(exist_ok=True)

    @classmethod
    def validate(cls) -> list[str]:
        """Validate configuration and return list of errors"""
        errors = []

        if not cls.SMTP_USERNAME:
            errors.append("SMTP_USERNAME is not set")
        if not cls.SMTP_PASSWORD:
            errors.append("SMTP_PASSWORD is not set")
        if not cls.SENDER_EMAIL:
            errors.append("SENDER_EMAIL is not set")

        return errors


# Initialize directories on import
Config.ensure_directories()
