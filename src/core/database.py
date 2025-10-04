"""SQLite database management"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from contextlib import contextmanager

from .config import Config
from .models import Company, GDPRRequest, RequestStatus, RequestType, WorkflowTask


class Database:
    """Database manager for GDPR requests"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Companies table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    website TEXT,
                    data_protection_officer TEXT,
                    address TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # GDPR requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gdpr_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    company_name TEXT NOT NULL,
                    request_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'draft',
                    subject TEXT NOT NULL,
                    body TEXT NOT NULL,
                    user_name TEXT,
                    user_email TEXT,
                    user_data TEXT,
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sent_at TIMESTAMP,
                    acknowledged_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    deadline TIMESTAMP,
                    reminder_count INTEGER DEFAULT 0,
                    last_reminder_at TIMESTAMP,
                    response_text TEXT,
                    notes TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies (id)
                )
            """)
            
            # Workflow tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workflow_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id INTEGER NOT NULL,
                    task_type TEXT NOT NULL,
                    scheduled_at TIMESTAMP NOT NULL,
                    executed_at TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    result TEXT,
                    error TEXT,
                    FOREIGN KEY (request_id) REFERENCES gdpr_requests (id)
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_requests_status ON gdpr_requests(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_requests_company ON gdpr_requests(company_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_scheduled ON workflow_tasks(scheduled_at)")
    
    # Company operations
    def add_company(self, company: Company) -> int:
        """Add a new company"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO companies (name, email, website, data_protection_officer, address, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (company.name, company.email, company.website, 
                  company.data_protection_officer, company.address, company.notes))
            return cursor.lastrowid
    
    def get_company(self, company_id: int) -> Optional[Company]:
        """Get company by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
            row = cursor.fetchone()
            return Company(**dict(row)) if row else None
    
    def get_company_by_name(self, name: str) -> Optional[Company]:
        """Get company by name"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies WHERE name = ?", (name,))
            row = cursor.fetchone()
            return Company(**dict(row)) if row else None
    
    def list_companies(self) -> List[Company]:
        """List all companies"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies ORDER BY name")
            return [Company(**dict(row)) for row in cursor.fetchall()]
    
    def update_company(self, company: Company):
        """Update company information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE companies 
                SET name = ?, email = ?, website = ?, data_protection_officer = ?,
                    address = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (company.name, company.email, company.website,
                  company.data_protection_officer, company.address, 
                  company.notes, company.id))
    
    # GDPR request operations
    def add_request(self, request: GDPRRequest) -> int:
        """Add a new GDPR request"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO gdpr_requests 
                (company_id, company_name, request_type, status, subject, body,
                 user_name, user_email, user_data, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (request.company_id, request.company_name, request.request_type.value,
                  request.status.value, request.subject, request.body,
                  request.user_name, request.user_email, 
                  str(request.user_data) if request.user_data else None,
                  request.reason))
            return cursor.lastrowid
    
    def get_request(self, request_id: int) -> Optional[GDPRRequest]:
        """Get request by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gdpr_requests WHERE id = ?", (request_id,))
            row = cursor.fetchone()
            if row:
                data = dict(row)
                data['request_type'] = RequestType(data['request_type'])
                data['status'] = RequestStatus(data['status'])
                return GDPRRequest(**data)
            return None
    
    def list_requests(self, status: Optional[RequestStatus] = None) -> List[GDPRRequest]:
        """List requests, optionally filtered by status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM gdpr_requests WHERE status = ? ORDER BY created_at DESC",
                             (status.value,))
            else:
                cursor.execute("SELECT * FROM gdpr_requests ORDER BY created_at DESC")
            
            requests = []
            for row in cursor.fetchall():
                data = dict(row)
                data['request_type'] = RequestType(data['request_type'])
                data['status'] = RequestStatus(data['status'])
                requests.append(GDPRRequest(**data))
            return requests
    
    def update_request_status(self, request_id: int, status: RequestStatus, 
                            notes: Optional[str] = None):
        """Update request status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            timestamp_field = None
            
            if status == RequestStatus.SENT:
                timestamp_field = "sent_at"
            elif status == RequestStatus.ACKNOWLEDGED:
                timestamp_field = "acknowledged_at"
            elif status == RequestStatus.COMPLETED:
                timestamp_field = "completed_at"
            
            if timestamp_field:
                cursor.execute(f"""
                    UPDATE gdpr_requests 
                    SET status = ?, {timestamp_field} = CURRENT_TIMESTAMP, notes = ?
                    WHERE id = ?
                """, (status.value, notes, request_id))
            else:
                cursor.execute("""
                    UPDATE gdpr_requests 
                    SET status = ?, notes = ?
                    WHERE id = ?
                """, (status.value, notes, request_id))
    
    def add_reminder(self, request_id: int):
        """Increment reminder count"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE gdpr_requests 
                SET reminder_count = reminder_count + 1,
                    last_reminder_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (request_id,))
    
    # Workflow task operations
    def add_task(self, task: WorkflowTask) -> int:
        """Add a workflow task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO workflow_tasks 
                (request_id, task_type, scheduled_at, status)
                VALUES (?, ?, ?, ?)
            """, (task.request_id, task.task_type, task.scheduled_at, task.status))
            return cursor.lastrowid
    
    def get_pending_tasks(self, before: Optional[datetime] = None) -> List[WorkflowTask]:
        """Get pending tasks scheduled before a certain time"""
        before = before or datetime.now()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM workflow_tasks 
                WHERE status = 'pending' AND scheduled_at <= ?
                ORDER BY scheduled_at
            """, (before,))
            return [WorkflowTask(**dict(row)) for row in cursor.fetchall()]
    
    def update_task_status(self, task_id: int, status: str, 
                          result: Optional[str] = None, error: Optional[str] = None):
        """Update task status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE workflow_tasks 
                SET status = ?, executed_at = CURRENT_TIMESTAMP, result = ?, error = ?
                WHERE id = ?
            """, (status, result, error, task_id))
