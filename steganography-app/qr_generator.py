#!/usr/bin/env python3
"""
PHANTOM QR CODE MODULE - CLASSIFIED
Advanced QR Code Generation with Metadata Embedding
Ghost Protocol QR Operations - Scannable Intelligence
"""

import qrcode
import json
import hashlib
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import base64
from logging_module import log_phantom_operation

class PhantomQRGenerator:
    """Elite QR code generation system with metadata embedding"""
    
    def __init__(self):
        self.output_dir = "phantom_qr_codes"
        self.temp_dir = "temp_qr_assets"
        self.setup_directories()
        
    def setup_directories(self):
        """Setup required directories"""
        for directory in [self.output_dir, self.temp_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def generate_metadata_qr(self, file_info, encryption_info=None, sender_info=None):
        """Generate QR code containing file metadata"""
        try:
            # Create metadata payload
            metadata = {
                'phantom_version': '3.0',
                'file_name': file_info.get('name', 'unknown'),
                'file_size': file_info.get('size', 0),
                'file_hash': file_info.get('hash', ''),
                'timestamp': datetime.now().isoformat(),
                'operation_id': hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:16]
            }
            
            # Add encryption info if provided
            if encryption_info:
                metadata['encryption'] = {
                    'method': encryption_info.get('method', 'AES-256'),
                    'key_hash': encryption_info.get('key_hash', ''),
                    'signature': encryption_info.get('signature', '')
                }
            
            # Add sender info if provided
            if sender_info:
                metadata['sender'] = {
                    'id': sender_info.get('id', 'ANONYMOUS'),
                    'email': sender_info.get('email', ''),
                    'public_key_hash': sender_info.get('public_key_hash', '')
                }
            
            # Convert to JSON
            metadata_json = json.dumps(metadata, separators=(',', ':'))
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
                box_size=10,
                border=4,
            )
            
            qr.add_data(metadata_json)
            qr.make(fit=True)
            
            # Create QR image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            qr_filename = f"phantom_metadata_{timestamp}.png"
            qr_path = os.path.join(self.output_dir, qr_filename)
            qr_image.save(qr_path)
            
            log_phantom_operation("METADATA_QR_GENERATED", {
                "qr_path": qr_path,
                "metadata_size": len(metadata_json),
                "operation_id": metadata['operation_id']
            })
            
            return qr_path, metadata
            
        except Exception as e:
            log_phantom_operation("METADATA_QR_ERROR", {"error": str(e)}, "ERROR")
            return None, None
    
    def generate_steganography_qr(self, stego_info):
        """Generate QR code for steganography operation info"""
        try:
            # Create steganography metadata
            stego_metadata = {
                'phantom_type': 'STEGANOGRAPHY',
                'cover_image': stego_info.get('cover_image', ''),
                'payload_type': stego_info.get('payload_type', 'text'),
                'embedding_method': 'LSB_ADVANCED',
                'stealth_level': stego_info.get('stealth_level', 5),
                'encryption_enabled': stego_info.get('encrypted', False),
                'noise_injection': stego_info.get('noise_added', False),
                'digital_signature': stego_info.get('signed', False),
                'timestamp': datetime.now().isoformat(),
                'verification_hash': hashlib.sha256(
                    f"{stego_info.get('cover_image', '')}{time.time()}".encode()
                ).hexdigest()[:32]
            }
            
            # Add extraction instructions
            stego_metadata['extraction_info'] = {
                'tool': 'Phantom Steganography Suite v3.0',
                'algorithm': 'Advanced LSB with Quantum Noise',
                'key_required': stego_info.get('encrypted', False),
                'instructions': 'Use Phantom Suite to extract hidden data'
            }
            
            # Convert to JSON
            stego_json = json.dumps(stego_metadata, separators=(',', ':'))
            
            # Create QR code with custom styling
            qr = qrcode.QRCode(
                version=2,  # Larger version for more data
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=4,
            )
            
            qr.add_data(stego_json)
            qr.make(fit=True)
            
            # Create styled QR image
            qr_image = qr.make_image(fill_color="#00ff00", back_color="#000000")  # Matrix style
            
            # Add Phantom branding
            branded_qr = self.add_phantom_branding(qr_image, "STEGANOGRAPHY")
            
            # Save QR code
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            qr_filename = f"phantom_stego_{timestamp}.png"
            qr_path = os.path.join(self.output_dir, qr_filename)
            branded_qr.save(qr_path)
            
            log_phantom_operation("STEGANOGRAPHY_QR_GENERATED", {
                "qr_path": qr_path,
                "verification_hash": stego_metadata['verification_hash']
            })
            
            return qr_path, stego_metadata
            
        except Exception as e:
            log_phantom_operation("STEGANOGRAPHY_QR_ERROR", {"error": str(e)}, "ERROR")
            return None, None
    
    def generate_contact_qr(self, contact_info):
        """Generate QR code for contact information"""
        try:
            # Create contact metadata
            contact_metadata = {
                'phantom_type': 'CONTACT',
                'user_id': contact_info.get('user_id', ''),
                'display_name': contact_info.get('name', ''),
                'email': contact_info.get('email', ''),
                'public_key': contact_info.get('public_key', ''),
                'phantom_version': '3.0',
                'capabilities': [
                    'STEGANOGRAPHY',
                    'ENCRYPTED_CHAT',
                    'SECURE_FILE_TRANSFER',
                    'VOICE_COMMANDS'
                ],
                'timestamp': datetime.now().isoformat(),
                'contact_hash': hashlib.sha256(
                    f"{contact_info.get('user_id', '')}{contact_info.get('email', '')}".encode()
                ).hexdigest()[:16]
            }
            
            # Convert to JSON
            contact_json = json.dumps(contact_metadata, separators=(',', ':'))
            
            # Create QR code
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            
            qr.add_data(contact_json)
            qr.make(fit=True)
            
            # Create contact QR image with blue theme
            qr_image = qr.make_image(fill_color="#0066ff", back_color="white")
            
            # Add contact branding
            branded_qr = self.add_phantom_branding(qr_image, "CONTACT")
            
            # Save QR code
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            qr_filename = f"phantom_contact_{timestamp}.png"
            qr_path = os.path.join(self.output_dir, qr_filename)
            branded_qr.save(qr_path)
            
            log_phantom_operation("CONTACT_QR_GENERATED", {
                "qr_path": qr_path,
                "contact_hash": contact_metadata['contact_hash']
            })
            
            return qr_path, contact_metadata
            
        except Exception as e:
            log_phantom_operation("CONTACT_QR_ERROR", {"error": str(e)}, "ERROR")
            return None, None
    
    def generate_network_info_qr(self, network_data):
        """Generate QR code for network scan results"""
        try:
            # Create network info metadata
            network_metadata = {
                'phantom_type': 'NETWORK_SCAN',
                'scan_id': network_data.get('scan_id', ''),
                'network_range': network_data.get('network_range', ''),
                'hosts_found': len(network_data.get('hosts_discovered', [])),
                'vulnerabilities': network_data.get('total_vulnerabilities', 0),
                'risk_level': network_data.get('risk_level', 'UNKNOWN'),
                'scan_timestamp': network_data.get('scan_start_time', ''),
                'scanner_version': 'Phantom Network Scanner v3.0',
                'report_available': True
            }
            
            # Convert to JSON
            network_json = json.dumps(network_metadata, separators=(',', ':'))
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            
            qr.add_data(network_json)
            qr.make(fit=True)
            
            # Create network QR image with red theme for security
            qr_image = qr.make_image(fill_color="#ff0000", back_color="white")
            
            # Add network branding
            branded_qr = self.add_phantom_branding(qr_image, "NETWORK")
            
            # Save QR code
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            qr_filename = f"phantom_network_{timestamp}.png"
            qr_path = os.path.join(self.output_dir, qr_filename)
            branded_qr.save(qr_path)
            
            log_phantom_operation("NETWORK_QR_GENERATED", {
                "qr_path": qr_path,
                "scan_id": network_metadata['scan_id']
            })
            
            return qr_path, network_metadata
            
        except Exception as e:
            log_phantom_operation("NETWORK_QR_ERROR", {"error": str(e)}, "ERROR")
            return None, None
    
    def add_phantom_branding(self, qr_image, qr_type):
        """Add Phantom branding to QR code"""
        try:
            # Convert to RGB if needed
            if qr_image.mode != 'RGB':
                qr_image = qr_image.convert('RGB')
            
            # Create new image with space for branding
            width, height = qr_image.size
            new_height = height + 60  # Add space for text
            
            branded_image = Image.new('RGB', (width, new_height), 'white')
            branded_image.paste(qr_image, (0, 0))
            
            # Add text
            draw = ImageDraw.Draw(branded_image)
            
            try:
                # Try to use a better font if available
                font_title = ImageFont.truetype("arial.ttf", 16)
                font_subtitle = ImageFont.truetype("arial.ttf", 12)
            except:
                # Fallback to default font
                font_title = ImageFont.load_default()
                font_subtitle = ImageFont.load_default()
            
            # Add title
            title_text = f"PHANTOM {qr_type}"
            title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, height + 5), title_text, fill='black', font=font_title)
            
            # Add subtitle
            subtitle_text = "Scan with Phantom Suite"
            subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            draw.text((subtitle_x, height + 25), subtitle_text, fill='gray', font=font_subtitle)
            
            # Add timestamp
            timestamp_text = datetime.now().strftime("%Y-%m-%d %H:%M")
            timestamp_bbox = draw.textbbox((0, 0), timestamp_text, font=font_subtitle)
            timestamp_width = timestamp_bbox[2] - timestamp_bbox[0]
            timestamp_x = (width - timestamp_width) // 2
            draw.text((timestamp_x, height + 40), timestamp_text, fill='gray', font=font_subtitle)
            
            return branded_image
            
        except Exception as e:
            log_phantom_operation("QR_BRANDING_ERROR", {"error": str(e)}, "WARNING")
            return qr_image
    
    def scan_qr_code(self, qr_image_path):
        """Scan and decode QR code"""
        try:
            from pyzbar import pyzbar
            
            # Load image
            image = Image.open(qr_image_path)
            
            # Decode QR codes
            decoded_objects = pyzbar.decode(image)
            
            if not decoded_objects:
                return None, "No QR code found in image"
            
            # Get first QR code data
            qr_data = decoded_objects[0].data.decode('utf-8')
            
            # Try to parse as JSON
            try:
                metadata = json.loads(qr_data)
                
                log_phantom_operation("QR_CODE_SCANNED", {
                    "qr_image": qr_image_path,
                    "data_type": metadata.get('phantom_type', 'UNKNOWN')
                })
                
                return metadata, None
                
            except json.JSONDecodeError:
                # Not JSON, return raw data
                return {'raw_data': qr_data}, None
                
        except ImportError:
            return None, "pyzbar library not installed. Install with: pip install pyzbar"
        except Exception as e:
            log_phantom_operation("QR_SCAN_ERROR", {"error": str(e)}, "ERROR")
            return None, str(e)
    
    def create_batch_qr_codes(self, data_list, qr_type="BATCH"):
        """Create multiple QR codes from a list of data"""
        try:
            qr_paths = []
            
            for i, data in enumerate(data_list):
                # Create individual QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=10,
                    border=4,
                )
                
                # Add batch info to data
                batch_data = {
                    'phantom_type': qr_type,
                    'batch_index': i,
                    'batch_total': len(data_list),
                    'data': data,
                    'timestamp': datetime.now().isoformat()
                }
                
                qr.add_data(json.dumps(batch_data, separators=(',', ':')))
                qr.make(fit=True)
                
                # Create QR image
                qr_image = qr.make_image(fill_color="black", back_color="white")
                
                # Add branding
                branded_qr = self.add_phantom_branding(qr_image, f"{qr_type} {i+1}/{len(data_list)}")
                
                # Save QR code
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                qr_filename = f"phantom_batch_{qr_type.lower()}_{i+1}_{timestamp}.png"
                qr_path = os.path.join(self.output_dir, qr_filename)
                branded_qr.save(qr_path)
                
                qr_paths.append(qr_path)
            
            log_phantom_operation("BATCH_QR_GENERATED", {
                "qr_count": len(qr_paths),
                "qr_type": qr_type
            })
            
            return qr_paths
            
        except Exception as e:
            log_phantom_operation("BATCH_QR_ERROR", {"error": str(e)}, "ERROR")
            return []
    
    def embed_qr_in_image(self, qr_path, background_image_path, output_path, position='bottom-right'):
        """Embed QR code into another image"""
        try:
            # Load images
            qr_image = Image.open(qr_path)
            background = Image.open(background_image_path)
            
            # Resize QR code if needed
            bg_width, bg_height = background.size
            qr_size = min(bg_width // 4, bg_height // 4, 200)  # Max 1/4 of background or 200px
            qr_image = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
            
            # Calculate position
            if position == 'bottom-right':
                x = bg_width - qr_size - 10
                y = bg_height - qr_size - 10
            elif position == 'bottom-left':
                x = 10
                y = bg_height - qr_size - 10
            elif position == 'top-right':
                x = bg_width - qr_size - 10
                y = 10
            elif position == 'top-left':
                x = 10
                y = 10
            else:  # center
                x = (bg_width - qr_size) // 2
                y = (bg_height - qr_size) // 2
            
            # Create a copy of background
            result_image = background.copy()
            
            # Paste QR code with transparency if available
            if qr_image.mode == 'RGBA':
                result_image.paste(qr_image, (x, y), qr_image)
            else:
                result_image.paste(qr_image, (x, y))
            
            # Save result
            result_image.save(output_path)
            
            log_phantom_operation("QR_EMBEDDED_IN_IMAGE", {
                "qr_path": qr_path,
                "background_path": background_image_path,
                "output_path": output_path,
                "position": position
            })
            
            return output_path
            
        except Exception as e:
            log_phantom_operation("QR_EMBED_ERROR", {"error": str(e)}, "ERROR")
            return None

# Global QR generator instance
phantom_qr_generator = None

def get_phantom_qr_generator():
    """Get global QR generator instance"""
    global phantom_qr_generator
    if phantom_qr_generator is None:
        phantom_qr_generator = PhantomQRGenerator()
    return phantom_qr_generator

if __name__ == "__main__":
    # Test the QR generator
    print("PHANTOM QR CODE GENERATOR - TEST MODE")
    print("="*50)
    
    generator = PhantomQRGenerator()
    
    # Test metadata QR generation
    test_file_info = {
        'name': 'secret_document.pdf',
        'size': 1024000,
        'hash': 'abc123def456'
    }
    
    test_encryption_info = {
        'method': 'AES-256',
        'key_hash': 'xyz789',
        'signature': 'signed_hash'
    }
    
    test_sender_info = {
        'id': 'GHOST_001',
        'email': 'ghost@phantom.secure'
    }
    
    qr_path, metadata = generator.generate_metadata_qr(
        test_file_info, test_encryption_info, test_sender_info
    )
    
    if qr_path:
        print(f"Test metadata QR generated: {qr_path}")
    
    print("\nPhantom QR generator ready for intelligence operations.")
