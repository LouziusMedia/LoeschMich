"""AI-powered GDPR request generator"""

from datetime import datetime
from typing import Dict, Optional

from ..core.models import Company, RequestType
from ..utils.logger import logger
from ..utils.templates import TemplateManager
from .ollama_client import OllamaClient


class RequestGenerator:
    """Generate personalized GDPR requests using AI"""

    def __init__(self, use_ai: bool = True):
        self.use_ai = use_ai
        self.ollama = OllamaClient() if use_ai else None

        if use_ai and self.ollama and not self.ollama.is_available():
            logger.warning("Ollama is not available. Falling back to templates.")
            self.use_ai = False

    def generate_deletion_request(
        self,
        company: Company,
        user_name: Optional[str] = None,
        user_email: Optional[str] = None,
        user_data: Optional[Dict[str, str]] = None,
        reason: Optional[str] = None,
        language: str = "de",
    ) -> tuple[str, str]:
        """
        Generate a deletion request
        Returns: (subject, body)
        """

        # Get subject
        subject = TemplateManager.get_subject(RequestType.DELETION, language)

        # If AI is enabled and reason is provided, enhance the request
        if self.use_ai and reason and self.ollama:
            body = self._generate_ai_enhanced_request(
                company=company,
                user_name=user_name,
                user_email=user_email,
                user_data=user_data,
                reason=reason,
                language=language,
            )
        else:
            # Use template
            body = TemplateManager.render_template(
                request_type=RequestType.DELETION,
                language=language,
                company_name=company.name,
                user_name=user_name,
                user_email=user_email,
                user_data=user_data,
                reason=reason,
            )

        return subject, body

    def _generate_ai_enhanced_request(
        self,
        company: Company,
        user_name: Optional[str],
        user_email: Optional[str],
        user_data: Optional[Dict[str, str]],
        reason: str,
        language: str,
    ) -> str:
        """Generate AI-enhanced request with better phrasing"""

        # Get base template
        base_template = TemplateManager.render_template(
            request_type=RequestType.DELETION,
            language=language,
            company_name=company.name,
            user_name=user_name,
            user_email=user_email,
            user_data=user_data,
            reason=reason,
        )

        # Create AI prompt
        system_prompt = """Du bist ein Experte für Datenschutzrecht und DSGVO.
Deine Aufgabe ist es, professionelle und rechtlich fundierte Löschanträge zu formulieren.
Behalte die rechtlichen Anforderungen bei, aber verbessere die Formulierung und Begründung."""

        user_prompt = f"""Verbessere folgenden DSGVO-Löschantrag, indem du:
1. Die Begründung präziser und überzeugender formulierst
2. Einen professionellen, aber bestimmten Ton beibehältst
3. Alle rechtlichen Anforderungen beibehältst
4. Die Struktur und formalen Elemente beibehältst

Ursprünglicher Antrag:
{base_template}

Verbesserte Version:"""

        try:
            enhanced = self.ollama.generate(
                prompt=user_prompt, system=system_prompt, temperature=0.7
            )

            if enhanced:
                logger.info("AI-enhanced request generated successfully")
                return enhanced
            else:
                logger.warning("AI generation failed, using template")
                return base_template

        except Exception as e:
            logger.error(f"AI enhancement failed: {e}")
            return base_template

    def generate_reminder(
        self,
        company: Company,
        original_date: datetime,
        user_name: Optional[str] = None,
        language: str = "de",
    ) -> tuple[str, str]:
        """
        Generate a reminder email
        Returns: (subject, body)
        """

        subject = TemplateManager.get_reminder_subject(language)
        body = TemplateManager.render_template(
            request_type="reminder",
            language=language,
            company_name=company.name,
            user_name=user_name,
            original_date=original_date.strftime("%d.%m.%Y"),
        )

        return subject, body

    def generate_escalation(
        self,
        company: Company,
        original_date: datetime,
        user_name: Optional[str] = None,
        language: str = "de",
    ) -> tuple[str, str]:
        """
        Generate an escalation email
        Returns: (subject, body)
        """

        subject = TemplateManager.get_escalation_subject(language)
        body = TemplateManager.render_template(
            request_type="escalation",
            language=language,
            company_name=company.name,
            user_name=user_name,
            original_date=original_date.strftime("%d.%m.%Y"),
        )

        return subject, body
