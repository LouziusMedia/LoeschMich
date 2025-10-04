"""AI-powered response analyzer"""

from enum import Enum
from typing import Any, Dict

from ..utils.logger import logger
from .ollama_client import OllamaClient


class ResponseType(str, Enum):
    """Type of company response"""

    ACKNOWLEDGED = "acknowledged"  # Company acknowledged the request
    COMPLETED = "completed"  # Deletion completed
    REJECTED = "rejected"  # Request rejected
    NEEDS_INFO = "needs_info"  # Company needs more information
    UNKNOWN = "unknown"  # Cannot determine


class ResponseAnalyzer:
    """Analyze company responses using AI"""

    def __init__(self, use_ai: bool = True):
        self.use_ai = use_ai
        self.ollama = OllamaClient() if use_ai else None

        if use_ai and self.ollama and not self.ollama.is_available():
            logger.warning(
                "Ollama is not available. Response analysis will be limited."
            )
            self.use_ai = False

    def analyze_response(self, response_text: str) -> Dict[str, Any]:
        """
        Analyze a company's response to a GDPR request

        Returns:
            {
                'type': ResponseType,
                'summary': str,
                'action_required': bool,
                'suggested_action': str,
                'confidence': float
            }
        """

        if not response_text or not response_text.strip():
            return {
                "type": ResponseType.UNKNOWN,
                "summary": "Empty response",
                "action_required": True,
                "suggested_action": "Wait for response or send reminder",
                "confidence": 1.0,
            }

        if self.use_ai and self.ollama:
            return self._ai_analyze(response_text)
        else:
            return self._keyword_analyze(response_text)

    def _ai_analyze(self, response_text: str) -> Dict[str, Any]:
        """Analyze response using AI"""

        system_prompt = """Du bist ein Experte für DSGVO und Datenschutzrecht.
Analysiere die Antwort eines Unternehmens auf einen DSGVO-Löschantrag.
Bestimme:
1. Den Typ der Antwort (acknowledged/completed/rejected/needs_info/unknown)
2. Eine kurze Zusammenfassung
3. Ob weitere Aktionen erforderlich sind
4. Welche Aktion empfohlen wird

Antworte im JSON-Format:
{
  "type": "acknowledged|completed|rejected|needs_info|unknown",
  "summary": "Kurze Zusammenfassung",
  "action_required": true|false,
  "suggested_action": "Empfohlene Aktion",
  "confidence": 0.0-1.0
}"""

        user_prompt = f"""Analysiere folgende Unternehmensantwort auf einen DSGVO-Löschantrag:

{response_text}

Analyse (JSON):"""

        try:
            result = self.ollama.generate(
                prompt=user_prompt, system=system_prompt, temperature=0.3
            )

            if result:
                # Try to parse JSON
                import json

                try:
                    # Extract JSON from response
                    json_start = result.find("{")
                    json_end = result.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = result[json_start:json_end]
                        analysis = json.loads(json_str)

                        # Validate and convert type
                        response_type = analysis.get("type", "unknown")
                        try:
                            analysis["type"] = ResponseType(response_type)
                        except ValueError:
                            analysis["type"] = ResponseType.UNKNOWN

                        logger.info(f"AI analysis: {analysis['type'].value}")
                        return analysis
                except json.JSONDecodeError:
                    logger.warning("Failed to parse AI response as JSON")

            # Fallback to keyword analysis
            return self._keyword_analyze(response_text)

        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._keyword_analyze(response_text)

    def _keyword_analyze(self, response_text: str) -> Dict[str, Any]:
        """Simple keyword-based analysis"""

        text_lower = response_text.lower()

        # Check for completion
        completion_keywords = [
            "gelöscht",
            "deleted",
            "entfernt",
            "removed",
            "vollständig gelöscht",
            "completely deleted",
        ]
        if any(kw in text_lower for kw in completion_keywords):
            return {
                "type": ResponseType.COMPLETED,
                "summary": "Daten wurden gelöscht",
                "action_required": False,
                "suggested_action": "Keine weitere Aktion erforderlich",
                "confidence": 0.7,
            }

        # Check for acknowledgment
        ack_keywords = [
            "bestätigen",
            "erhalten",
            "bearbeiten",
            "prüfen",
            "acknowledge",
            "received",
            "processing",
        ]
        if any(kw in text_lower for kw in ack_keywords):
            return {
                "type": ResponseType.ACKNOWLEDGED,
                "summary": "Anfrage wurde bestätigt",
                "action_required": True,
                "suggested_action": "Warten auf Abschluss, ggf. Erinnerung senden",
                "confidence": 0.6,
            }

        # Check for rejection
        rejection_keywords = [
            "ablehnen",
            "abgelehnt",
            "nicht möglich",
            "nicht erfüllen",
            "reject",
            "rejected",
            "cannot",
            "can not",
            "unable",
            "gesetzliche aufbewahrungspflicht",
            "gesetzlichen aufbewahrungspflichten",
            "aufbewahrungspflicht",
            "aufbewahrungspflichten",
            "legal obligation",
            "legal obligations",
            "retention obligation",
            "retention obligations",
        ]
        if any(kw in text_lower for kw in rejection_keywords):
            return {
                "type": ResponseType.REJECTED,
                "summary": "Anfrage wurde abgelehnt",
                "action_required": True,
                "suggested_action": "Begründung prüfen, ggf. Beschwerde einreichen",
                "confidence": 0.7,
            }

        # Check for information request
        info_keywords = [
            "weitere informationen",
            "more information",
            "identifizierung",
            "identification",
            "nachweis",
            "proof",
        ]
        if any(kw in text_lower for kw in info_keywords):
            return {
                "type": ResponseType.NEEDS_INFO,
                "summary": "Unternehmen benötigt weitere Informationen",
                "action_required": True,
                "suggested_action": "Angeforderte Informationen bereitstellen",
                "confidence": 0.6,
            }

        # Unknown
        return {
            "type": ResponseType.UNKNOWN,
            "summary": "Antworttyp konnte nicht bestimmt werden",
            "action_required": True,
            "suggested_action": "Manuelle Prüfung erforderlich",
            "confidence": 0.3,
        }
