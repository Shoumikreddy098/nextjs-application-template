#!/usr/bin/env python3
"""
PHANTOM FILE UTILITIES MODULE - CLASSIFIED
Advanced File Operations with Security Features
Ghost Protocol File Management - Secure and Stealthy
"""

import os
import sys
import shutil
import zipfile
import hashlib
import json
import time
from datetime import datetime
import tempfile
import threading
from pathlib import Path
from cryptography.fernet import Fernet
import base64
from logging_module import log_phantom_operation, log_phantom_security

class PhantomFileManager:
    """Elite file management system with security features"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='phantom_files_')
        self.secure_delete_passes = 7  # DoD 5220.22-M standard
        self.compression_level = 9
        self.max_file_size = 100 * 1024 * 1024  # 100MB default limit
        
    def create_secure_zip(self, file_paths, output_path, password=None, compression_level=None):
        """Create secure ZIP archive with optional encryption"""
        try:
            if compression_level is None:
                compression_level = self.compression_level
            
            # Validate input files
            valid_files = []
            total_size = 0
            
            for file_path in file_paths:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    valid_files.append((file_path, file_size))
                else:
                    log_phantom_operation("INVALID_FILE_SKIPPED", {
                        "file_path": file_path
                    }, "WARNING")
            
            if not valid_files:
                raise ValueError("No valid files to archive")
            
            if total_size > self.max_file_size:
                log_phantom_operation("ARCHIVE_SIZE_WARNING", {
                    "total_size": total_size,
                    "max_size": self.max_file_size
                }, "WARNING")
            
            # Create ZIP archive
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
                for file_path, file_size in valid_files:
                    # Get relative path for archive
                    arcname = os.path.basename(file_path)
                    
                    # Add file to archive
                    zipf.write(file_path, arcname)
                    
                    log_phantom_operation("FILE_ADDED_TO_ARCHIVE", {
                        "file_path": file_path,
                        "archive_name": arcname,
                        "file_size": file_size
                    })
                
                # Add metadata file
                metadata = {
                    'phantom_version': '3.0',
                    'created_by': 'Phantom File Manager',
                    'creation_time': datetime.now().isoformat(),
                    'file_count': len(valid_files),
                    'total_size': total_size,
                    'compression_level': compression_level,
                    'encrypted': password is not None
                }
                
                metadata_json = json.dumps(metadata, indent=2)
                zipf.writestr('phantom_metadata.json', metadata_json)
            
            # Apply password protection if requested
            if password:
                encrypted_path = self.encrypt_file(output_path, password)
                if encrypted_path:
                    # Replace original with encrypted version
                    shutil.move(encrypted_path, output_path)
                    log_phantom_security("ARCHIVE_ENCRYPTED", "INFO", {
                        "archive_path": output_path
                    })
            
            archive_info = {
                'archive_path': output_path,
                'file_count': len(valid_files),
                'total_size': total_size,
                'compressed_size': os.path.getsize(output_path),
                'compression_ratio': (1 - os.path.getsize(output_path) / total_size) * 100 if total_size > 0 else 0,
                'encrypted': password is not None
            }
            
            log_phantom_operation("SECURE_ARCHIVE_CREATED", archive_info)
            
            return True, archive_info
            
        except Exception as e:
            log_phantom_operation("SECURE_ARCHIVE_ERROR", {"error": str(e)}, "ERROR")
            return False, str(e)
    
    def extract_secure_zip(self, archive_path, output_dir, password=None):
        """Extract secure ZIP archive with optional decryption"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Decrypt archive if password provided
            archive_to_extract = archive_path
            if password:
                decrypted_path = self.decrypt_file(archive_path, password)
                if not decrypted_path:
                    raise ValueError("Failed to decrypt archive")
                archive_to_extract = decrypted_path
            
            extracted_files = []
            
            # Extract ZIP archive
            with zipfile.ZipFile(archive_to_extract, 'r') as zipf:
                # Check for metadata
                metadata = None
                if 'phantom_metadata.json' in zipf.namelist():
                    metadata_content = zipf.read('phantom_metadata.json').decode('utf-8')
                    metadata = json.loads(metadata_content)
                    
                    log_phantom_operation("ARCHIVE_METADATA_FOUND", metadata)
                
                # Extract all files
                for file_info in zipf.filelist:
                    if file_info.filename != 'phantom_metadata.json':
                        extracted_path = zipf.extract(file_info, output_dir)
                        extracted_files.append(extracted_path)
                        
                        log_phantom_operation("FILE_EXTRACTED", {
                            "file_name": file_info.filename,
                            "extracted_path": extracted_path,
                            "file_size": file_info.file_size
                        })
            
            # Clean up temporary decrypted file
            if password and archive_to_extract != archive_path:
                self.secure_delete_file(archive_to_extract)
            
            extraction_info = {
                'archive_path': archive_path,
                'output_dir': output_dir,
                'extracted_files': extracted_files,
                'file_count': len(extracted_files),
                'metadata': metadata
            }
            
            log_phantom_operation("SECURE_EXTRACTION_COMPLETED", extraction_info)
            
            return True, extraction_info
            
        except Exception as e:
            log_phantom_operation("SECURE_EXTRACTION_ERROR", {"error": str(e)}, "ERROR")
            return False, str(e)
    
    def encrypt_file(self, file_path, password):
        """Encrypt file with password"""
        try:
            # Generate key from password
            key = self.derive_key_from_password(password)
            cipher = Fernet(key)
            
            # Read file content
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Encrypt data
            encrypted_data = cipher.encrypt(file_data)
            
            # Create encrypted file
            encrypted_path = file_path + '.phantom_encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            log_phantom_security("FILE_ENCRYPTED", "INFO", {
                "original_path": file_path,
                "encrypted_path": encrypted_path,
                "original_size": len(file_data),
                "encrypted_size": len(encrypted_data)
            })
            
            return encrypted_path
            
        except Exception as e:
            log_phantom_security("FILE_ENCRYPTION_ERROR", "ERROR", {"error": str(e)})
            return None
    
    def decrypt_file(self, encrypted_file_path, password):
        """Decrypt file with password"""
        try:
            # Generate key from password
            key = self.derive_key_from_password(password)
            cipher = Fernet(key)
            
            # Read encrypted file
            with open(encrypted_file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Create decrypted file
            if encrypted_file_path.endswith('.phantom_encrypted'):
                decrypted_path = encrypted_file_path[:-18]  # Remove .phantom_encrypted
            else:
                decrypted_path = encrypted_file_path + '.decrypted'
            
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_data)
            
            log_phantom_security("FILE_DECRYPTED", "INFO", {
                "encrypted_path": encrypted_file_path,
                "decrypted_path": decrypted_path,
                "encrypted_size": len(encrypted_data),
                "decrypted_size": len(decrypted_data)
            })
            
            return decrypted_path
            
        except Exception as e:
            log_phantom_security("FILE_DECRYPTION_ERROR", "ERROR", {"error": str(e)})
            return None
    
    def derive_key_from_password(self, password):
        """Derive encryption key from password"""
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        salt = b"PHANTOM_FILE_SALT_2024"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def calculate_file_hash(self, file_path, algorithm='sha256'):
        """Calculate file hash"""
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            file_hash = hash_obj.hexdigest()
            
            log_phantom_operation("FILE_HASH_CALCULATED", {
                "file_path": file_path,
                "algorithm": algorithm,
                "hash": file_hash
            })
            
            return file_hash
            
        except Exception as e:
            log_phantom_operation("FILE_HASH_ERROR", {"error": str(e)}, "ERROR")
            return None
    
    def secure_delete_file(self, file_path):
        """Securely delete file using multiple overwrite passes"""
        try:
            if not os.path.exists(file_path):
                return True
            
            file_size = os.path.getsize(file_path)
            
            log_phantom_security("SECURE_DELETE_STARTED", "WARNING", {
                "file_path": file_path,
                "file_size": file_size,
                "passes": self.secure_delete_passes
            })
            
            # Perform multiple overwrite passes
            with open(file_path, 'r+b') as f:
                for pass_num in range(self.secure_delete_passes):
                    f.seek(0)
                    
                    # Different patterns for each pass
                    if pass_num == 0:
                        pattern = b'\x00' * file_size  # Zeros
                    elif pass_num == 1:
                        pattern = b'\xFF' * file_size  # Ones
                    elif pass_num == 2:
                        pattern = os.urandom(file_size)  # Random
                    else:
                        # Alternating patterns
                        pattern = (b'\xAA' if pass_num % 2 == 0 else b'\x55') * file_size
                    
                    f.write(pattern[:file_size])
                    f.flush()
                    os.fsync(f.fileno())  # Force write to disk
            
            # Finally delete the file
            os.remove(file_path)
            
            log_phantom_security("SECURE_DELETE_COMPLETED", "WARNING", {
                "file_path": file_path,
                "passes_completed": self.secure_delete_passes
            })
            
            return True
            
        except Exception as e:
            log_phantom_security("SECURE_DELETE_ERROR", "ERROR", {"error": str(e)})
            return False
    
    def split_file(self, file_path, chunk_size_mb=10):
        """Split large file into smaller chunks"""
        try:
            chunk_size = chunk_size_mb * 1024 * 1024  # Convert to bytes
            file_size = os.path.getsize(file_path)
            
            if file_size <= chunk_size:
                log_phantom_operation("FILE_SPLIT_NOT_NEEDED", {
                    "file_path": file_path,
                    "file_size": file_size,
                    "chunk_size": chunk_size
                })
                return [file_path]
            
            base_name = os.path.splitext(file_path)[0]
            extension = os.path.splitext(file_path)[1]
            
            chunk_paths = []
            chunk_num = 1
            
            with open(file_path, 'rb') as input_file:
                while True:
                    chunk_data = input_file.read(chunk_size)
                    if not chunk_data:
                        break
                    
                    chunk_path = f"{base_name}.part{chunk_num:03d}{extension}"
                    
                    with open(chunk_path, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)
                    
                    chunk_paths.append(chunk_path)
                    chunk_num += 1
            
            # Create manifest file
            manifest = {
                'original_file': os.path.basename(file_path),
                'original_size': file_size,
                'chunk_size': chunk_size,
                'chunk_count': len(chunk_paths),
                'chunks': [os.path.basename(path) for path in chunk_paths],
                'created_at': datetime.now().isoformat(),
                'file_hash': self.calculate_file_hash(file_path)
            }
            
            manifest_path = f"{base_name}.phantom_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            log_phantom_operation("FILE_SPLIT_COMPLETED", {
                "original_file": file_path,
                "chunk_count": len(chunk_paths),
                "manifest_path": manifest_path
            })
            
            return chunk_paths + [manifest_path]
            
        except Exception as e:
            log_phantom_operation("FILE_SPLIT_ERROR", {"error": str(e)}, "ERROR")
            return []
    
    def join_file_chunks(self, manifest_path):
        """Join file chunks back into original file"""
        try:
            # Read manifest
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            original_file = manifest['original_file']
            chunk_count = manifest['chunk_count']
            expected_size = manifest['original_size']
            original_hash = manifest.get('file_hash')
            
            # Get directory of manifest
            manifest_dir = os.path.dirname(manifest_path)
            output_path = os.path.join(manifest_dir, original_file)
            
            # Join chunks
            with open(output_path, 'wb') as output_file:
                for chunk_name in manifest['chunks']:
                    chunk_path = os.path.join(manifest_dir, chunk_name)
                    
                    if not os.path.exists(chunk_path):
                        raise FileNotFoundError(f"Chunk file not found: {chunk_path}")
                    
                    with open(chunk_path, 'rb') as chunk_file:
                        output_file.write(chunk_file.read())
            
            # Verify file integrity
            actual_size = os.path.getsize(output_path)
            if actual_size != expected_size:
                raise ValueError(f"Size mismatch: expected {expected_size}, got {actual_size}")
            
            if original_hash:
                actual_hash = self.calculate_file_hash(output_path)
                if actual_hash != original_hash:
                    raise ValueError(f"Hash mismatch: expected {original_hash}, got {actual_hash}")
            
            log_phantom_operation("FILE_JOIN_COMPLETED", {
                "output_path": output_path,
                "chunk_count": chunk_count,
                "file_size": actual_size,
                "integrity_verified": True
            })
            
            return output_path
            
        except Exception as e:
            log_phantom_operation("FILE_JOIN_ERROR", {"error": str(e)}, "ERROR")
            return None
    
    def get_file_info(self, file_path):
        """Get comprehensive file information"""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat_info = os.stat(file_path)
            
            file_info = {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': stat_info.st_size,
                'size_human': self.format_file_size(stat_info.st_size),
                'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                'permissions': oct(stat_info.st_mode)[-3:],
                'is_file': os.path.isfile(file_path),
                'is_directory': os.path.isdir(file_path),
                'extension': os.path.splitext(file_path)[1].lower(),
                'hash_sha256': self.calculate_file_hash(file_path) if os.path.isfile(file_path) else None
            }
            
            return file_info
            
        except Exception as e:
            log_phantom_operation("FILE_INFO_ERROR", {"error": str(e)}, "ERROR")
            return None
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.temp_dir = tempfile.mkdtemp(prefix='phantom_files_')
            
            log_phantom_operation("TEMP_FILES_CLEANED", {
                "temp_dir": self.temp_dir
            })
            
        except Exception as e:
            log_phantom_operation("TEMP_CLEANUP_ERROR", {"error": str(e)}, "WARNING")

# Global file manager instance
phantom_file_manager = None

def get_phantom_file_manager():
    """Get global file manager instance"""
    global phantom_file_manager
    if phantom_file_manager is None:
        phantom_file_manager = PhantomFileManager()
    return phantom_file_manager

if __name__ == "__main__":
    # Test the file manager
    print("PHANTOM FILE MANAGER - TEST MODE")
    print("="*50)
    
    file_manager = PhantomFileManager()
    
    # Test file info
    test_file = __file__  # This script itself
    file_info = file_manager.get_file_info(test_file)
    
    if file_info:
        print(f"File: {file_info['name']}")
        print(f"Size: {file_info['size_human']}")
        print(f"Hash: {file_info['hash_sha256'][:16]}...")
    
    print("\nPhantom file manager ready for secure operations.")
