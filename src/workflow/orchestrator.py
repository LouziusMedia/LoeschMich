"""Workflow orchestrator for managing GDPR request lifecycle"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from ..ai.request_generator import RequestGenerator
from ..ai.response_analyzer import ResponseAnalyzer, ResponseType
from ..communication.email_sender import EmailSender
from ..core.config import Config
from ..core.database import Database
from ..core.models import Company, GDPRRequest, RequestStatus, WorkflowTask
from ..utils.logger import logger


class WorkflowOrchestrator:
    """Orchestrate the GDPR request workflow"""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()
        self.request_generator = RequestGenerator()
        self.response_analyzer = ResponseAnalyzer()
        self.email_sender = EmailSender()

    def create_and_send_request(
        self,
        company: Company,
        user_name: Optional[str] = None,
        user_email: Optional[str] = None,
        user_data: Optional[Dict[str, str]] = None,
        reason: Optional[str] = None,
        language: str = "de",
        auto_send: bool = False,
    ) -> Optional[int]:
        """
        Create a GDPR deletion request and optionally send it

        Returns:
            Request ID if successful, None otherwise
        """

        # Generate request
        subject, body = self.request_generator.generate_deletion_request(
            company=company,
            user_name=user_name,
            user_email=user_email,
            user_data=user_data,
            reason=reason,
            language=language,
        )

        # Create request in database
        from ..core.models import RequestType

        request = GDPRRequest(
            company_id=company.id,
            company_name=company.name,
            request_type=RequestType.DELETION,
            status=RequestStatus.DRAFT,
            subject=subject,
            body=body,
            user_name=user_name,
            user_email=user_email,
            user_data=user_data,
            reason=reason,
        )

        request_id = self.db.add_request(request)
        logger.info(f"Created request {request_id} for {company.name}")

        # Send if auto_send is enabled
        if auto_send or Config.AUTO_SEND_ENABLED:
            success = self.send_request(request_id)
            if not success:
                logger.warning(f"Failed to send request {request_id}")

        return request_id

    def send_request(self, request_id: int) -> bool:
        """Send a GDPR request via email"""

        request = self.db.get_request(request_id)
        if not request:
            logger.error(f"Request {request_id} not found")
            return False

        company = self.db.get_company(request.company_id)
        if not company:
            logger.error(f"Company {request.company_id} not found")
            return False

        # Send email
        success = self.email_sender.send_email(
            to_email=company.email, subject=request.subject, body=request.body
        )

        if success:
            # Update status
            self.db.update_request_status(
                request_id,
                RequestStatus.SENT,
                notes=f"Sent at {datetime.now().isoformat()}",
            )

            # Schedule follow-up tasks
            self._schedule_followup_tasks(request_id)

            logger.info(f"Request {request_id} sent successfully")
            return True
        else:
            self.db.update_request_status(
                request_id, RequestStatus.FAILED, notes="Failed to send email"
            )
            return False

    def _schedule_followup_tasks(self, request_id: int):
        """Schedule automatic follow-up tasks"""

        # Schedule reminder after RETRY_DELAY_DAYS
        reminder_date = datetime.now() + timedelta(days=Config.RETRY_DELAY_DAYS)
        reminder_task = WorkflowTask(
            request_id=request_id,
            task_type="send_reminder",
            scheduled_at=reminder_date,
            status="pending",
        )
        self.db.add_task(reminder_task)
        logger.info(f"Scheduled reminder for request {request_id} at {reminder_date}")

        # Schedule escalation after ESCALATION_DELAY_DAYS
        escalation_date = datetime.now() + timedelta(days=Config.ESCALATION_DELAY_DAYS)
        escalation_task = WorkflowTask(
            request_id=request_id,
            task_type="send_escalation",
            scheduled_at=escalation_date,
            status="pending",
        )
        self.db.add_task(escalation_task)
        logger.info(
            f"Scheduled escalation for request {request_id} at {escalation_date}"
        )

    def send_reminder(self, request_id: int) -> bool:
        """Send a reminder for a pending request"""

        request = self.db.get_request(request_id)
        if not request:
            logger.error(f"Request {request_id} not found")
            return False

        # Don't send reminder if already completed
        if request.status in [RequestStatus.COMPLETED, RequestStatus.REJECTED]:
            logger.info(
                f"Request {request_id} already {request.status.value}, skipping reminder"
            )
            return False

        company = self.db.get_company(request.company_id)
        if not company:
            logger.error(f"Company {request.company_id} not found")
            return False

        # Generate reminder
        subject, body = self.request_generator.generate_reminder(
            company=company,
            original_date=request.sent_at or request.created_at,
            user_name=request.user_name,
        )

        # Send email
        success = self.email_sender.send_email(
            to_email=company.email, subject=subject, body=body
        )

        if success:
            self.db.add_reminder(request_id)
            logger.info(f"Reminder sent for request {request_id}")
            return True
        else:
            logger.error(f"Failed to send reminder for request {request_id}")
            return False

    def send_escalation(self, request_id: int) -> bool:
        """Send an escalation for an unresolved request"""

        request = self.db.get_request(request_id)
        if not request:
            logger.error(f"Request {request_id} not found")
            return False

        # Don't escalate if already completed
        if request.status in [RequestStatus.COMPLETED, RequestStatus.REJECTED]:
            logger.info(
                f"Request {request_id} already {request.status.value}, skipping escalation"
            )
            return False

        company = self.db.get_company(request.company_id)
        if not company:
            logger.error(f"Company {request.company_id} not found")
            return False

        # Generate escalation
        subject, body = self.request_generator.generate_escalation(
            company=company,
            original_date=request.sent_at or request.created_at,
            user_name=request.user_name,
        )

        # Send email
        success = self.email_sender.send_email(
            to_email=company.email, subject=subject, body=body
        )

        if success:
            self.db.update_request_status(
                request_id,
                RequestStatus.ESCALATED,
                notes=f"Escalated at {datetime.now().isoformat()}",
            )
            logger.info(f"Escalation sent for request {request_id}")
            return True
        else:
            logger.error(f"Failed to send escalation for request {request_id}")
            return False

    def process_response(self, request_id: int, response_text: str) -> Dict[str, Any]:
        """Process a company's response"""

        # Analyze response
        analysis = self.response_analyzer.analyze_response(response_text)

        # Update request based on analysis
        request = self.db.get_request(request_id)
        if not request:
            logger.error(f"Request {request_id} not found")
            return analysis

        # Map response type to request status
        status_mapping = {
            ResponseType.ACKNOWLEDGED: RequestStatus.ACKNOWLEDGED,
            ResponseType.COMPLETED: RequestStatus.COMPLETED,
            ResponseType.REJECTED: RequestStatus.REJECTED,
            ResponseType.NEEDS_INFO: RequestStatus.PENDING,
        }

        new_status = status_mapping.get(analysis["type"], request.status)

        # Update database
        self.db.update_request_status(
            request_id, new_status, notes=f"Response analyzed: {analysis['summary']}"
        )

        # Store response text
        from ..core.database import Database

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE gdpr_requests SET response_text = ? WHERE id = ?",
                (response_text, request_id),
            )

        logger.info(
            f"Response processed for request {request_id}: {analysis['type'].value}"
        )

        return analysis

    def execute_pending_tasks(self) -> int:
        """Execute all pending workflow tasks"""

        tasks = self.db.get_pending_tasks()
        executed_count = 0

        for task in tasks:
            try:
                logger.info(f"Executing task {task.id}: {task.task_type}")

                if task.task_type == "send_reminder":
                    success = self.send_reminder(task.request_id)
                elif task.task_type == "send_escalation":
                    success = self.send_escalation(task.request_id)
                else:
                    logger.warning(f"Unknown task type: {task.task_type}")
                    success = False

                # Update task status
                if success:
                    self.db.update_task_status(task.id, "completed", result="Success")
                    executed_count += 1
                else:
                    self.db.update_task_status(
                        task.id, "failed", error="Execution failed"
                    )

            except Exception as e:
                logger.error(f"Error executing task {task.id}: {e}")
                self.db.update_task_status(task.id, "failed", error=str(e))

        logger.info(f"Executed {executed_count}/{len(tasks)} tasks")
        return executed_count
