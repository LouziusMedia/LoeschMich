"""Email sender using SMTP"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from datetime import datetime

from ..core.config import Config
from ..utils.logger import logger


class EmailSender:
    """Send emails via SMTP"""
    
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.username = Config.SMTP_USERNAME
        self.password = Config.SMTP_PASSWORD
        self.sender_email = Config.SENDER_EMAIL
        self.sender_name = Config.SENDER_NAME
    
    def validate_config(self) -> bool:
        """Validate SMTP configuration"""
        if not all([self.smtp_server, self.smtp_port, self.username, 
                   self.password, self.sender_email]):
            logger.error("SMTP configuration is incomplete")
            return False
        return True
    
    def send_email(self,
                  to_email: str,
                  subject: str,
                  body: str,
                  cc: Optional[List[str]] = None,
                  bcc: Optional[List[str]] = None,
                  html: bool = False) -> bool:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            html: Whether body is HTML
            
        Returns:
            True if sent successfully, False otherwise
        """
        
        if not self.validate_config():
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.sender_email}>" if self.sender_name else self.sender_email
            msg['To'] = to_email
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Attach body
            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, mime_type, 'utf-8'))
            
            # Send email
            logger.info(f"Sending email to {to_email}")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                server.send_message(msg, self.sender_email, recipients)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email to {to_email}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email to {to_email}: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection"""
        if not self.validate_config():
            return False
        
        try:
            logger.info("Testing SMTP connection...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.username, self.password)
            logger.info("SMTP connection successful")
            return True
        except smtplib.SMTPException as e:
            logger.error(f"SMTP connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error testing SMTP: {e}")
            return False
