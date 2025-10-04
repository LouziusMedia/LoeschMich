#!/usr/bin/env python3
"""
GDPR Deletion Request Automation Tool
Main CLI application
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.database import Database
from src.core.models import Company, RequestStatus, RequestType
from src.core.config import Config
from src.workflow.orchestrator import WorkflowOrchestrator
from src.communication.email_sender import EmailSender
from src.ai.ollama_client import OllamaClient
from src.utils.logger import logger


def cmd_add_company(args):
    """Add a new company"""
    db = Database()
    
    company = Company(
        name=args.name,
        email=args.email,
        website=args.website,
        data_protection_officer=args.dpo,
        address=args.address,
        notes=args.notes
    )
    
    company_id = db.add_company(company)
    logger.info(f"✓ Company '{args.name}' added with ID {company_id}")
    print(f"Company added successfully (ID: {company_id})")


def cmd_list_companies(args):
    """List all companies"""
    db = Database()
    companies = db.list_companies()
    
    if not companies:
        print("No companies found.")
        return
    
    print(f"\n{'ID':<5} {'Name':<30} {'Email':<40}")
    print("-" * 80)
    for company in companies:
        print(f"{company.id:<5} {company.name:<30} {company.email:<40}")
    print(f"\nTotal: {len(companies)} companies")


def cmd_create_request(args):
    """Create a GDPR deletion request"""
    db = Database()
    orchestrator = WorkflowOrchestrator(db)
    
    # Get company
    if args.company_id:
        company = db.get_company(args.company_id)
    else:
        company = db.get_company_by_name(args.company)
    
    if not company:
        logger.error(f"Company not found: {args.company or args.company_id}")
        print("Error: Company not found")
        return
    
    # Create request
    request_id = orchestrator.create_and_send_request(
        company=company,
        user_name=args.user_name,
        user_email=args.user_email,
        reason=args.reason,
        language=args.language,
        auto_send=args.send
    )
    
    if request_id:
        status = "created and sent" if args.send else "created"
        logger.info(f"✓ Request {status} for {company.name}")
        print(f"Request {status} successfully (ID: {request_id})")
    else:
        print("Error: Failed to create request")


def cmd_send_request(args):
    """Send a pending request"""
    db = Database()
    orchestrator = WorkflowOrchestrator(db)
    
    if args.all:
        # Send all pending requests
        requests = db.list_requests(RequestStatus.DRAFT)
        sent_count = 0
        
        for request in requests:
            if orchestrator.send_request(request.id):
                sent_count += 1
        
        print(f"Sent {sent_count}/{len(requests)} requests")
    else:
        # Send specific request
        success = orchestrator.send_request(args.id)
        if success:
            print(f"Request {args.id} sent successfully")
        else:
            print(f"Error: Failed to send request {args.id}")


def cmd_status(args):
    """Show status of all requests"""
    db = Database()
    
    if args.id:
        # Show specific request
        request = db.get_request(args.id)
        if not request:
            print(f"Request {args.id} not found")
            return
        
        print(f"\nRequest ID: {request.id}")
        print(f"Company: {request.company_name}")
        print(f"Type: {request.request_type.value}")
        print(f"Status: {request.status.value}")
        print(f"Created: {request.created_at}")
        if request.sent_at:
            print(f"Sent: {request.sent_at}")
        if request.reminder_count > 0:
            print(f"Reminders sent: {request.reminder_count}")
        if request.notes:
            print(f"Notes: {request.notes}")
    else:
        # Show all requests
        requests = db.list_requests()
        
        if not requests:
            print("No requests found.")
            return
        
        print(f"\n{'ID':<5} {'Company':<25} {'Type':<12} {'Status':<12} {'Created':<20}")
        print("-" * 80)
        for request in requests:
            created = request.created_at.strftime("%Y-%m-%d %H:%M") if isinstance(request.created_at, datetime) else str(request.created_at)[:16]
            print(f"{request.id:<5} {request.company_name[:24]:<25} {request.request_type.value:<12} {request.status.value:<12} {created:<20}")
        print(f"\nTotal: {len(requests)} requests")


def cmd_process_response(args):
    """Process a company response"""
    db = Database()
    orchestrator = WorkflowOrchestrator(db)
    
    # Read response from file or stdin
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            response_text = f.read()
    else:
        print("Enter the company's response (Ctrl+D when done):")
        response_text = sys.stdin.read()
    
    # Process response
    analysis = orchestrator.process_response(args.id, response_text)
    
    print(f"\nResponse Analysis:")
    print(f"Type: {analysis['type'].value}")
    print(f"Summary: {analysis['summary']}")
    print(f"Action required: {analysis['action_required']}")
    print(f"Suggested action: {analysis['suggested_action']}")
    print(f"Confidence: {analysis['confidence']:.0%}")


def cmd_auto_followup(args):
    """Execute automatic follow-up tasks"""
    db = Database()
    orchestrator = WorkflowOrchestrator(db)
    
    executed = orchestrator.execute_pending_tasks()
    print(f"Executed {executed} pending tasks")


def cmd_test_smtp(args):
    """Test SMTP connection"""
    sender = EmailSender()
    
    if sender.test_connection():
        print("✓ SMTP connection successful")
    else:
        print("✗ SMTP connection failed")
        print("Please check your .env configuration")


def cmd_test_ollama(args):
    """Test Ollama connection"""
    client = OllamaClient()
    
    if client.is_available():
        print("✓ Ollama is running")
        models = client.list_models()
        if models:
            print(f"Available models: {', '.join(models)}")
        else:
            print("No models found. Run: ollama pull llama2")
    else:
        print("✗ Ollama is not running")
        print("Please start Ollama: https://ollama.ai")


def cmd_init(args):
    """Initialize the application"""
    print("Initializing GDPR Deletion Tool...")
    
    # Create directories
    Config.ensure_directories()
    print("✓ Directories created")
    
    # Initialize database
    db = Database()
    print("✓ Database initialized")
    
    # Validate configuration
    errors = Config.validate()
    if errors:
        print("\n⚠ Configuration warnings:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease configure your .env file")
    else:
        print("✓ Configuration valid")
    
    # Test connections
    print("\nTesting connections...")
    
    sender = EmailSender()
    if sender.validate_config():
        if sender.test_connection():
            print("✓ SMTP connection successful")
        else:
            print("✗ SMTP connection failed")
    else:
        print("⚠ SMTP not configured")
    
    client = OllamaClient()
    if client.is_available():
        print("✓ Ollama is running")
    else:
        print("⚠ Ollama is not running (optional)")
    
    print("\n✓ Initialization complete!")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="GDPR Deletion Request Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # init command
    parser_init = subparsers.add_parser('init', help='Initialize the application')
    parser_init.set_defaults(func=cmd_init)
    
    # add-company command
    parser_add = subparsers.add_parser('add-company', help='Add a new company')
    parser_add.add_argument('--name', required=True, help='Company name')
    parser_add.add_argument('--email', required=True, help='Contact email')
    parser_add.add_argument('--website', help='Company website')
    parser_add.add_argument('--dpo', help='Data Protection Officer')
    parser_add.add_argument('--address', help='Company address')
    parser_add.add_argument('--notes', help='Additional notes')
    parser_add.set_defaults(func=cmd_add_company)
    
    # list-companies command
    parser_list = subparsers.add_parser('list-companies', help='List all companies')
    parser_list.set_defaults(func=cmd_list_companies)
    
    # create-request command
    parser_create = subparsers.add_parser('create-request', help='Create a GDPR deletion request')
    parser_create.add_argument('--company', help='Company name')
    parser_create.add_argument('--company-id', type=int, help='Company ID')
    parser_create.add_argument('--user-name', help='Your name')
    parser_create.add_argument('--user-email', help='Your email')
    parser_create.add_argument('--reason', help='Reason for deletion')
    parser_create.add_argument('--language', default='de', choices=['de', 'en'], help='Language')
    parser_create.add_argument('--send', action='store_true', help='Send immediately')
    parser_create.set_defaults(func=cmd_create_request)
    
    # send-request command
    parser_send = subparsers.add_parser('send-request', help='Send a pending request')
    parser_send.add_argument('--id', type=int, help='Request ID')
    parser_send.add_argument('--all', action='store_true', help='Send all pending requests')
    parser_send.set_defaults(func=cmd_send_request)
    
    # status command
    parser_status = subparsers.add_parser('status', help='Show request status')
    parser_status.add_argument('--id', type=int, help='Request ID (show details)')
    parser_status.set_defaults(func=cmd_status)
    
    # process-response command
    parser_response = subparsers.add_parser('process-response', help='Process company response')
    parser_response.add_argument('--id', type=int, required=True, help='Request ID')
    parser_response.add_argument('--file', help='Response file path')
    parser_response.set_defaults(func=cmd_process_response)
    
    # auto-followup command
    parser_followup = subparsers.add_parser('auto-followup', help='Execute automatic follow-ups')
    parser_followup.set_defaults(func=cmd_auto_followup)
    
    # test-smtp command
    parser_smtp = subparsers.add_parser('test-smtp', help='Test SMTP connection')
    parser_smtp.set_defaults(func=cmd_test_smtp)
    
    # test-ollama command
    parser_ollama = subparsers.add_parser('test-ollama', help='Test Ollama connection')
    parser_ollama.set_defaults(func=cmd_test_ollama)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    try:
        args.func(args)
    except Exception as e:
        logger.error(f"Command failed: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
