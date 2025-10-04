"""GDPR request templates based on datenanfragen.de"""

from datetime import datetime
from typing import Dict, Optional

from jinja2 import Template

from ..core.models import RequestType

# German deletion request template (Art. 17 DSGVO)
DELETION_REQUEST_DE = """Sehr geehrte Damen und Herren{% if company_name %} der {{ company_name }}{% endif %},

ich stelle hiermit Antrag auf unverzügliche Löschung mich betreffender personenbezogener Daten gemäß Art. 17 DSGVO.

{% if reason %}
Begründung: {{ reason }}
{% endif %}

Sofern ich eine Einwilligung zur Verarbeitung meiner Daten erteilt habe (z. B. gemäß Art. 6 Abs. 1 lit. a oder Art. 9 Abs. 2 lit. a DSGVO), widerrufe ich diese hiermit.

Bitte bestätigen Sie mir die Löschung schriftlich.

Falls Sie meine personenbezogenen Daten an Dritte offengelegt haben, haben Sie meinen Wunsch auf Löschung der betreffenden personenbezogenen Daten sowie sämtlicher Verweise darauf nach Art. 17 Abs. 2 DSGVO allen Empfängern mitzuteilen. Bitte informieren Sie mich weiterhin über diese Empfänger.

Sofern Sie meinem Antrag nicht innerhalb der Frist von einem Monat nachkommen, behalte ich mir vor rechtliche Schritte gegen Sie einzuleiten und Beschwerde bei der zuständigen Datenschutzaufsichtsbehörde einzureichen.

Zur Identifikation meiner Person habe ich folgende Daten beigefügt:
{% if user_name %}Name: {{ user_name }}{% endif %}
{% if user_email %}E-Mail: {{ user_email }}{% endif %}
{% if user_data %}
{% for key, value in user_data.items() %}{{ key }}: {{ value }}
{% endfor %}
{% endif %}

Mit freundlichen Grüßen
{% if user_name %}{{ user_name }}{% endif %}

Datum: {{ date }}
"""

# English deletion request template (Art. 17 GDPR)
DELETION_REQUEST_EN = """Dear Sir or Madam,

I am hereby requesting immediate deletion of personal data concerning me according to Article 17 GDPR.

{% if reason %}
Reason: {{ reason }}
{% endif %}

If I have given consent to the processing of my personal data (e.g. according to Article 6(1) lit. a or Article 9(2) lit. a GDPR), I am hereby withdrawing said consent.

Please confirm the deletion in writing.

If you have disclosed the personal data in question to third parties, you have to communicate my request for erasure of the personal data concerned, as well as any references to it, to each recipient as laid down in Article 17(2) GDPR. Please also inform me about those recipients.

If you do not comply with my request within the period stated above, I am reserving the right to take legal action against you and to lodge a complaint with the responsible supervisory authority.

For identification purposes, I have included the following data:
{% if user_name %}Name: {{ user_name }}{% endif %}
{% if user_email %}Email: {{ user_email }}{% endif %}
{% if user_data %}
{% for key, value in user_data.items() %}{{ key }}: {{ value }}
{% endfor %}
{% endif %}

Yours sincerely,
{% if user_name %}{{ user_name }}{% endif %}

Date: {{ date }}
"""

# German reminder template
REMINDER_DE = """Sehr geehrte Damen und Herren,

am {{ original_date }} habe ich einen Antrag auf Löschung meiner personenbezogenen Daten gemäß Art. 17 DSGVO gestellt.

Gemäß Art. 12 Abs. 3 DSGVO haben Sie mir unverzüglich, spätestens aber innerhalb eines Monats nach Eingang des Antrags, die Informationen über die ergriffenen Maßnahmen zur Verfügung zu stellen.

Diese Frist ist mittlerweile abgelaufen. Ich fordere Sie hiermit auf, meinem Antrag unverzüglich nachzukommen.

Sollte ich innerhalb der nächsten zwei Wochen keine Antwort von Ihnen erhalten, behalte ich mir vor, rechtliche Schritte gegen Sie einzuleiten und Beschwerde bei der zuständigen Datenschutzaufsichtsbehörde einzureichen.

Mit freundlichen Grüßen
{% if user_name %}{{ user_name }}{% endif %}

Datum: {{ date }}
"""

# German escalation template
ESCALATION_DE = """Sehr geehrte Damen und Herren,

trotz mehrfacher Aufforderung haben Sie meinem Antrag auf Löschung meiner personenbezogenen Daten gemäß Art. 17 DSGVO (ursprünglich gestellt am {{ original_date }}) nicht entsprochen.

Dies stellt einen Verstoß gegen die DSGVO dar. Ich sehe mich daher gezwungen, Beschwerde bei der zuständigen Datenschutzaufsichtsbehörde einzureichen und rechtliche Schritte zu prüfen.

Ich fordere Sie letztmalig auf, meinem Antrag innerhalb von 7 Tagen nachzukommen und mir dies schriftlich zu bestätigen.

Mit freundlichen Grüßen
{% if user_name %}{{ user_name }}{% endif %}

Datum: {{ date }}
"""


class TemplateManager:
    """Manage GDPR request templates"""

    TEMPLATES = {
        (RequestType.DELETION, "de"): DELETION_REQUEST_DE,
        (RequestType.DELETION, "en"): DELETION_REQUEST_EN,
        ("reminder", "de"): REMINDER_DE,
        ("escalation", "de"): ESCALATION_DE,
    }

    @classmethod
    def render_template(cls, request_type: RequestType | str, language: str = "de", **kwargs) -> str:
        """Render a template with given variables"""

        template_key = (request_type, language)
        template_str = cls.TEMPLATES.get(template_key)

        if not template_str:
            raise ValueError(f"Template not found for {request_type} in {language}")

        template = Template(template_str)

        # Add default date if not provided
        if "date" not in kwargs:
            kwargs["date"] = datetime.now().strftime("%d.%m.%Y")

        return template.render(**kwargs)

    @classmethod
    def get_subject(cls, request_type: RequestType, language: str = "de") -> str:
        """Get email subject for request type"""

        subjects = {
            (RequestType.DELETION, "de"): "DSGVO Löschantrag gemäß Art. 17 DSGVO",
            (
                RequestType.DELETION,
                "en",
            ): "GDPR Deletion Request according to Art. 17 GDPR",
            (RequestType.ACCESS, "de"): "DSGVO Auskunftsantrag gemäß Art. 15 DSGVO",
            (RequestType.ACCESS, "en"): "GDPR Access Request according to Art. 15 GDPR",
        }

        return subjects.get((request_type, language), "DSGVO Antrag")

    @classmethod
    def get_reminder_subject(cls, language: str = "de") -> str:
        """Get reminder email subject"""
        if language == "de":
            return "Erinnerung: DSGVO Löschantrag"
        return "Reminder: GDPR Deletion Request"

    @classmethod
    def get_escalation_subject(cls, language: str = "de") -> str:
        """Get escalation email subject"""
        if language == "de":
            return "Letzte Mahnung: DSGVO Löschantrag"
        return "Final Notice: GDPR Deletion Request"
