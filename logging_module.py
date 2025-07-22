#!/usr/bin/env python3
"""
PHANTOM LOGGING MODULE - TOP SECRET
Advanced Logging System with Quantum Encryption
Ghost Protocol Activated - All Activities Monitored
"""

import os
import sys
import logging
import json
import hashlib
import time
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text
from rich.panel import Panel
import threading
import queue

class PhantomLogger:
    """Elite logging system with encryption and stealth capabilities"""
    
    def __init__(self, log_dir="phantom_logs", encryption_key=None):
        self.log_dir = log_dir
        self.console = Console()
        self.log_queue = queue.Queue()
        self.encryption_key = encryption_key or self.generate_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.session_id = self.generate_session_id()
        self.setup_logging_directory()
        self.setup_loggers()
        self.start_log_processor()
        
    def generate_encryption_key(self):
        """Generate encryption key for log files"""
        password = b"PHANTOM_GHOST_PROTOCOL_2024"
        salt = b"CLASSIFIED_SALT_PHANTOM"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def generate_session_id(self):
        """Generate unique session ID"""
        timestamp = str(time.time())
        user = os.getlogin()
        machine = os.uname().nodename if hasattr(os, 'uname') else 'UNKNOWN'
        session_data = f"{timestamp}_{user}_{machine}"
        return hashlib.sha256(session_data.encode()).hexdigest()[:16].upper()
    
    def setup_logging_directory(self):
        """Setup secure logging directory structure"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # Create subdirectories
        subdirs = ['system', 'operations', 'security', 'network', 'encrypted']
        for subdir in subdirs:
            path = os.path.join(self.log_dir, subdir)
            if not os.path.exists(path):
                os.makedirs(path)
    
    def setup_loggers(self):
        """Setup multiple specialized loggers"""
        # Main system logger
        self.system_logger = logging.getLogger('phantom.system')
        self.system_logger.setLevel(logging.DEBUG)
        
        # Operations logger
        self.ops_logger = logging.getLogger('phantom.operations')
        self.ops_logger.setLevel(logging.INFO)
        
        # Security logger
        self.security_logger = logging.getLogger('phantom.security')
        self.security_logger.setLevel(logging.WARNING)
        
        # Network logger
        self.network_logger = logging.getLogger('phantom.network')
        self.network_logger.setLevel(logging.INFO)
        
        # Setup handlers
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup logging handlers with encryption"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # System log handler
        system_handler = EncryptedFileHandler(
            os.path.join(self.log_dir, 'system', f'phantom_system_{timestamp}.log'),
            self.cipher_suite
        )
        system_formatter = PhantomFormatter('SYSTEM')
        system_handler.setFormatter(system_formatter)
        self.system_logger.addHandler(system_handler)
        
        # Operations log handler
        ops_handler = EncryptedFileHandler(
            os.path.join(self.log_dir, 'operations', f'phantom_ops_{timestamp}.log'),
            self.cipher_suite
        )
        ops_formatter = PhantomFormatter('OPERATIONS')
        ops_handler.setFormatter(ops_formatter)
        self.ops_logger.addHandler(ops_handler)
        
        # Security log handler
        security_handler = EncryptedFileHandler(
            os.path.join(self.log_dir, 'security', f'phantom_security_{timestamp}.log'),
            self.cipher_suite
        )
        security_formatter = PhantomFormatter('SECURITY')
        security_handler.setFormatter(security_formatter)
        self.security_logger.addHandler(security_handler)
        
        # Network log handler
        network_handler = EncryptedFileHandler(
            os.path.join(self.log_dir, 'network', f'phantom_network_{timestamp}.log'),
            self.cipher_suite
        )
        network_formatter = PhantomFormatter('NETWORK')
        network_handler.setFormatter(network_formatter)
        self.network_logger.addHandler(network_handler)
        
        # Console handler with Rich formatting
        console_handler = RichHandler(console=self.console, rich_tracebacks=True)
        console_formatter = PhantomConsoleFormatter()
        console_handler.setFormatter(console_formatter)
        
        # Add console handler to all loggers
        for logger in [self.system_logger, self.ops_logger, self.security_logger, self.network_logger]:
            logger.addHandler(console_handler)
    
    def start_log_processor(self):
        """Start background log processing thread"""
        self.log_processor_thread = threading.Thread(target=self.process_logs, daemon=True)
        self.log_processor_thread.start()
    
    def process_logs(self):
        """Process logs in background thread"""
        while True:
            try:
                log_entry = self.log_queue.get(timeout=1)
                self.write_encrypted_log(log_entry)
                self.log_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Log processing error: {e}")
    
    def write_encrypted_log(self, log_entry):
        """Write encrypted log entry to master log"""
        master_log_path = os.path.join(self.log_dir, 'encrypted', 'phantom_master.enc')
        
        # Encrypt log entry
        encrypted_entry = self.cipher_suite.encrypt(json.dumps(log_entry).encode())
        
        with open(master_log_path, 'ab') as f:
            f.write(encrypted_entry + b'\n')
    
    def log_system_event(self, message, level="INFO", category="GENERAL"):
        """Log system events"""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'session_id': self.session_id,
            'level': level,
            'category': category,
            'message': message,
            'type': 'SYSTEM'
        }
        
        self.log_queue.put(log_entry)
        
        if level == "CRITICAL":
            self.system_logger.critical(message)
        elif level == "ERROR":
            self.system_logger.error(message)
        elif level == "WARNING":
            self.system_logger.warning(message)
        elif level == "SUCCESS":
            self.system_logger.info(f"✓ {message}")
        else:
            self.system_logger.info(message)
    
    def log_operation(self, operation, details, status="SUCCESS"):
        """Log steganography operations"""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'session_id': self.session_id,
            'operation': operation,
            'details': details,
            'status': status,
            'type': 'OPERATION'
        }
        
        self.log_queue.put(log_entry)
        self.ops_logger.info(f"{operation}: {status}")
    
    def log_security_event(self, event, threat_level="LOW", details=None):
        """Log security events"""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'session_id': self.session_id,
            'event': event,
            'threat_level': threat_level,
            'details': details or {},
            'type': 'SECURITY'
        }
        
        self.log_queue.put(log_entry)
        
        if threat_level == "CRITICAL":
            self.security_logger.critical(f"🚨 SECURITY ALERT: {event}")
        elif threat_level == "HIGH":
            self.security_logger.error(f"⚠️ SECURITY WARNING: {event}")
        else:
            self.security_logger.warning(f"🔒 SECURITY EVENT: {event}")
    
    def log_network_activity(self, activity, source, destination=None, protocol=None):
        """Log network activities"""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'session_id': self.session_id,
            'activity': activity,
            'source': source,
            'destination': destination,
            'protocol': protocol,
            'type': 'NETWORK'
        }
        
        self.log_queue.put(log_entry)
        self.network_logger.info(f"NETWORK: {activity} - {source}")
    
    def get_session_logs(self):
        """Get logs for current session"""
        logs = []
        master_log_path = os.path.join(self.log_dir, 'encrypted', 'phantom_master.enc')
        
        if os.path.exists(master_log_path):
            try:
                with open(master_log_path, 'rb') as f:
                    for line in f:
                        if line.strip():
                            try:
                                decrypted = self.cipher_suite.decrypt(line.strip())
                                log_entry = json.loads(decrypted.decode())
                                if log_entry.get('session_id') == self.session_id:
                                    logs.append(log_entry)
                            except Exception:
                                continue
            except Exception as e:
                self.log_system_event(f"Error reading session logs: {e}", "ERROR")
        
        return logs
    
    def emergency_wipe(self):
        """Emergency log wipe for stealth operations"""
        try:
            import shutil
            if os.path.exists(self.log_dir):
                shutil.rmtree(self.log_dir)
            self.console.print("[red]🔥 EMERGENCY LOG WIPE COMPLETED[/red]")
        except Exception as e:
            self.console.print(f"[red]❌ Emergency wipe failed: {e}[/red]")

class EncryptedFileHandler(logging.FileHandler):
    """Custom file handler with encryption"""
    
    def __init__(self, filename, cipher_suite):
        super().__init__(filename)
        self.cipher_suite = cipher_suite
    
    def emit(self, record):
        """Emit encrypted log record"""
        try:
            msg = self.format(record)
            encrypted_msg = self.cipher_suite.encrypt(msg.encode())
            
            with open(self.baseFilename, 'ab') as f:
                f.write(encrypted_msg + b'\n')
        except Exception:
            self.handleError(record)

class PhantomFormatter(logging.Formatter):
    """Custom formatter for Phantom logs"""
    
    def __init__(self, module_name):
        self.module_name = module_name
        super().__init__()
    
    def format(self, record):
        """Format log record with Phantom styling"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        level = record.levelname
        message = record.getMessage()
        
        formatted = f"[{timestamp}] [{self.module_name}] [{level}] {message}"
        
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted

class PhantomConsoleFormatter(logging.Formatter):
    """Console formatter with colors"""
    
    def format(self, record):
        """Format for console output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        level = record.levelname
        message = record.getMessage()
        
        # Color coding
        if level == "CRITICAL":
            return f"🔴 [{timestamp}] {message}"
        elif level == "ERROR":
            return f"❌ [{timestamp}] {message}"
        elif level == "WARNING":
            return f"⚠️ [{timestamp}] {message}"
        elif "SUCCESS" in message or "✓" in message:
            return f"✅ [{timestamp}] {message}"
        else:
            return f"ℹ️ [{timestamp}] {message}"

def setup_phantom_logging(log_dir="phantom_logs"):
    """Setup the Phantom logging system"""
    logger = PhantomLogger(log_dir)
    
    # Display initialization banner
    logger.console.print(Panel.fit(
        "[bold green]PHANTOM LOGGING SYSTEM INITIALIZED[/bold green]\n"
        f"[cyan]Session ID: {logger.session_id}[/cyan]\n"
        f"[yellow]Log Directory: {log_dir}[/yellow]\n"
        "[red]⚠️ ALL ACTIVITIES ARE MONITORED ⚠️[/red]",
        title="[bold red]CLASSIFIED LOGGING[/bold red]",
        border_style="red"
    ))
    
    logger.log_system_event("PHANTOM LOGGING SYSTEM ACTIVATED", "SUCCESS", "INITIALIZATION")
    
    return logger

# Global logger instance
phantom_logger = None

def get_phantom_logger():
    """Get global phantom logger instance"""
    global phantom_logger
    if phantom_logger is None:
        phantom_logger = setup_phantom_logging()
    return phantom_logger

def log_phantom_event(message, level="INFO", category="GENERAL"):
    """Quick logging function"""
    logger = get_phantom_logger()
    logger.log_system_event(message, level, category)

def log_phantom_operation(operation, details, status="SUCCESS"):
    """Quick operation logging"""
    logger = get_phantom_logger()
    logger.log_operation(operation, details, status)

def log_phantom_security(event, threat_level="LOW", details=None):
    """Quick security logging"""
    logger = get_phantom_logger()
    logger.log_security_event(event, threat_level, details)

def log_phantom_network(activity, source, destination=None, protocol=None):
    """Quick network logging"""
    logger = get_phantom_logger()
    logger.log_network_activity(activity, source, destination, protocol)

if __name__ == "__main__":
    # Test the logging system
    logger = setup_phantom_logging()
    
    logger.log_system_event("Testing Phantom Logging System", "INFO")
    logger.log_operation("STEGANOGRAPHY_EMBED", {"file": "test.jpg", "payload": "secret.txt"}, "SUCCESS")
    logger.log_security_event("UNAUTHORIZED_ACCESS_ATTEMPT", "HIGH", {"ip": "192.168.1.100"})
    logger.log_network_activity("PORT_SCAN", "192.168.1.1", "192.168.1.100", "TCP")
    
    print("\n" + "="*50)
    print("SESSION LOGS:")
    print("="*50)
    
    for log in logger.get_session_logs():
        print(json.dumps(log, indent=2))
