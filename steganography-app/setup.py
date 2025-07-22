#!/usr/bin/env python3
"""
PHANTOM STEGANOGRAPHY SUITE SETUP SCRIPT
Advanced Installation and Configuration System
"""

import os
import sys
import subprocess
import platform
import json
from datetime import datetime

class PhantomSetup:
    """Elite setup system for Phantom Steganography Suite"""
    
    def __init__(self):
        self.system_info = {
            'os': platform.system(),
            'python_version': platform.python_version(),
            'architecture': platform.architecture()[0],
            'machine': platform.machine()
        }
        self.required_python_version = (3, 8)
        self.setup_log = []
        
    def print_banner(self):
        """Print epic setup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    PHANTOM SETUP v3.0                       ║
║              Advanced Installation System                    ║
║                                                              ║
║  ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ║
║  ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗  ║
║  ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔║
║  ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝║
║  ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ║
║  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ║
║                                                              ║
║           CLASSIFIED - UNAUTHORIZED ACCESS PROHIBITED        ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"🔥 Welcome to the most BADASS steganography suite ever created! 🔥")
        print(f"📅 Setup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💻 System: {self.system_info['os']} {self.system_info['architecture']}")
        print(f"🐍 Python: {self.system_info['python_version']}")
        print("="*70)
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🔍 Checking Python version...")
        
        current_version = sys.version_info[:2]
        if current_version < self.required_python_version:
            print(f"❌ ERROR: Python {self.required_python_version[0]}.{self.required_python_version[1]}+ required")
            print(f"   Current version: {current_version[0]}.{current_version[1]}")
            return False
        
        print(f"✅ Python version check passed: {sys.version}")
        self.setup_log.append("Python version check: PASSED")
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("\n📦 Installing dependencies...")
        
        try:
            # Upgrade pip first
            print("🔧 Upgrading pip...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            
            # Install requirements
            if os.path.exists('requirements.txt'):
                print("📋 Installing from requirements.txt...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                print("✅ Core dependencies installed successfully!")
            else:
                print("⚠️  requirements.txt not found, installing core packages...")
                core_packages = [
                    'PyQt5>=5.15.0',
                    'pillow>=8.0.0',
                    'opencv-python>=4.5.0',
                    'cryptography>=3.4.0',
                    'numpy>=1.20.0',
                    'matplotlib>=3.3.0',
                    'fpdf>=2.5.0',
                    'qrcode>=7.0.0',
                    'requests>=2.25.0',
                    'psutil>=5.8.0'
                ]
                
                for package in core_packages:
                    print(f"📦 Installing {package}...")
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            
            self.setup_log.append("Dependencies installation: SUCCESS")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            self.setup_log.append(f"Dependencies installation: FAILED - {e}")
            return False
    
    def install_optional_packages(self):
        """Install optional packages for enhanced features"""
        print("\n🎯 Installing optional packages for enhanced features...")
        
        optional_packages = {
            'speechrecognition': 'Voice command support',
            'pyaudio': 'Audio input for voice commands',
            'face-recognition': 'Advanced biometric authentication',
            'dlib': 'Face recognition backend',
            'pyzbar': 'QR code scanning',
            'scapy': 'Advanced network operations',
            'python-nmap': 'Network scanning',
            'gtts': 'Text-to-speech for voice responses',
            'pygame': 'Audio effects and sound'
        }
        
        installed_optional = []
        failed_optional = []
        
        for package, description in optional_packages.items():
            try:
                print(f"📦 Installing {package} ({description})...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                installed_optional.append(package)
                print(f"✅ {package} installed successfully!")
            except subprocess.CalledProcessError:
                failed_optional.append(package)
                print(f"⚠️  {package} installation failed (optional)")
        
        print(f"\n📊 Optional packages summary:")
        print(f"   ✅ Installed: {len(installed_optional)}")
        print(f"   ⚠️  Failed: {len(failed_optional)}")
        
        if failed_optional:
            print(f"   Failed packages: {', '.join(failed_optional)}")
            print("   Note: These are optional and won't prevent the app from running")
        
        self.setup_log.append(f"Optional packages: {len(installed_optional)} installed, {len(failed_optional)} failed")
        return True
    
    def create_directories(self):
        """Create necessary directories"""
        print("\n📁 Creating directory structure...")
        
        directories = [
            'phantom_logs',
            'phantom_logs/system',
            'phantom_logs/operations',
            'phantom_logs/security',
            'phantom_logs/network',
            'phantom_logs/encrypted',
            'phantom_reports',
            'phantom_qr_codes',
            'temp_report_assets',
            'temp_qr_assets',
            'report_templates'
        ]
        
        created_dirs = []
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                created_dirs.append(directory)
                print(f"📂 Created: {directory}")
            except Exception as e:
                print(f"❌ Failed to create {directory}: {e}")
        
        print(f"✅ Created {len(created_dirs)} directories")
        self.setup_log.append(f"Directory creation: {len(created_dirs)} directories created")
        return True
    
    def create_config_files(self):
        """Create default configuration files"""
        print("\n⚙️  Creating configuration files...")
        
        # Main configuration
        config = {
            'phantom_version': '3.0',
            'setup_date': datetime.now().isoformat(),
            'system_info': self.system_info,
            'features': {
                'voice_commands': True,
                'biometric_auth': True,
                'network_scanning': True,
                'steganography': True,
                'encrypted_chat': True,
                'pdf_reports': True,
                'qr_operations': True
            },
            'security': {
                'max_failed_attempts': 3,
                'lockout_duration_minutes': 5,
                'secure_delete_passes': 7,
                'encryption_algorithm': 'AES-256',
                'stealth_mode_enabled': True
            },
            'ui': {
                'theme': 'cyberpunk',
                'matrix_effects': True,
                'sound_effects': True,
                'animations': True
            }
        }
        
        try:
            with open('phantom_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            print("✅ Created phantom_config.json")
            
            # Create sample cover images info
            sample_info = {
                'info': 'Place cover images in this directory for steganography operations',
                'supported_formats': ['.png', '.bmp', '.tiff', '.jpg', '.jpeg'],
                'recommended_size': '800x600 or larger',
                'note': 'Larger images provide more capacity for hidden data'
            }
            
            os.makedirs('cover_images', exist_ok=True)
            with open('cover_images/README.txt', 'w') as f:
                f.write("PHANTOM COVER IMAGES DIRECTORY\n")
                f.write("="*40 + "\n\n")
                f.write("Place your cover images here for steganography operations.\n")
                f.write("Supported formats: PNG, BMP, TIFF, JPG, JPEG\n")
                f.write("Recommended size: 800x600 or larger\n")
                f.write("Larger images = more capacity for hidden data\n")
            
            self.setup_log.append("Configuration files: CREATED")
            return True
            
        except Exception as e:
            print(f"❌ Error creating config files: {e}")
            self.setup_log.append(f"Configuration files: FAILED - {e}")
            return False
    
    def test_installation(self):
        """Test the installation by importing key modules"""
        print("\n🧪 Testing installation...")
        
        test_modules = [
            ('PyQt5.QtWidgets', 'GUI framework'),
            ('PIL', 'Image processing'),
            ('cv2', 'Computer vision'),
            ('cryptography.fernet', 'Encryption'),
            ('numpy', 'Numerical operations'),
            ('matplotlib.pyplot', 'Plotting'),
            ('fpdf', 'PDF generation'),
            ('qrcode', 'QR code generation')
        ]
        
        passed_tests = 0
        failed_tests = []
        
        for module, description in test_modules:
            try:
                __import__(module)
                print(f"✅ {module} ({description})")
                passed_tests += 1
            except ImportError as e:
                print(f"❌ {module} ({description}) - {e}")
                failed_tests.append(module)
        
        print(f"\n📊 Test Results:")
        print(f"   ✅ Passed: {passed_tests}/{len(test_modules)}")
        print(f"   ❌ Failed: {len(failed_tests)}")
        
        if failed_tests:
            print(f"   Failed modules: {', '.join(failed_tests)}")
            print("   Some features may not work properly.")
        
        self.setup_log.append(f"Installation test: {passed_tests}/{len(test_modules)} modules passed")
        return len(failed_tests) == 0
    
    def create_launcher_scripts(self):
        """Create launcher scripts for different platforms"""
        print("\n🚀 Creating launcher scripts...")
        
        try:
            # Windows batch file
            if self.system_info['os'] == 'Windows':
                with open('launch_phantom.bat', 'w') as f:
                    f.write('@echo off\n')
                    f.write('title PHANTOM STEGANOGRAPHY SUITE\n')
                    f.write('echo Starting Phantom Steganography Suite...\n')
                    f.write('python main.py\n')
                    f.write('pause\n')
                print("✅ Created launch_phantom.bat (Windows)")
            
            # Unix shell script
            with open('launch_phantom.sh', 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('echo "Starting Phantom Steganography Suite..."\n')
                f.write('python3 main.py\n')
            
            # Make shell script executable
            if self.system_info['os'] in ['Linux', 'Darwin']:
                os.chmod('launch_phantom.sh', 0o755)
                print("✅ Created launch_phantom.sh (Unix/Linux/Mac)")
            
            # Python launcher (cross-platform)
            with open('launch_phantom.py', 'w') as f:
                f.write('#!/usr/bin/env python3\n')
                f.write('"""\n')
                f.write('PHANTOM STEGANOGRAPHY SUITE LAUNCHER\n')
                f.write('Cross-platform launcher script\n')
                f.write('"""\n\n')
                f.write('import os\n')
                f.write('import sys\n')
                f.write('import subprocess\n\n')
                f.write('def main():\n')
                f.write('    print("🔥 PHANTOM STEGANOGRAPHY SUITE v3.0 🔥")\n')
                f.write('    print("Launching elite hacker interface...")\n')
                f.write('    try:\n')
                f.write('        subprocess.run([sys.executable, "main.py"])\n')
                f.write('    except KeyboardInterrupt:\n')
                f.write('        print("\\n👻 Phantom protocol deactivated. Goodbye, Agent.")\n')
                f.write('    except Exception as e:\n')
                f.write('        print(f"❌ Launch error: {e}")\n\n')
                f.write('if __name__ == "__main__":\n')
                f.write('    main()\n')
            
            print("✅ Created launch_phantom.py (Cross-platform)")
            self.setup_log.append("Launcher scripts: CREATED")
            return True
            
        except Exception as e:
            print(f"❌ Error creating launcher scripts: {e}")
            self.setup_log.append(f"Launcher scripts: FAILED - {e}")
            return False
    
    def generate_setup_report(self):
        """Generate setup completion report"""
        print("\n📋 Generating setup report...")
        
        report = {
            'phantom_setup_report': {
                'version': '3.0',
                'setup_date': datetime.now().isoformat(),
                'system_info': self.system_info,
                'setup_log': self.setup_log,
                'status': 'COMPLETED',
                'next_steps': [
                    'Run: python main.py',
                    'Or use launcher scripts',
                    'Check README.md for usage instructions',
                    'Test voice commands: "Phantom, system status"',
                    'Explore the cyberpunk interface'
                ]
            }
        }
        
        try:
            with open('phantom_setup_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            print("✅ Setup report saved to phantom_setup_report.json")
            return True
            
        except Exception as e:
            print(f"❌ Error generating setup report: {e}")
            return False
    
    def print_completion_message(self):
        """Print epic completion message"""
        completion_banner = """
╔══════════════════════════════════════════════════════════════╗
║                    SETUP COMPLETED! 🎉                      ║
║                                                              ║
║  🔥 PHANTOM STEGANOGRAPHY SUITE IS READY FOR ACTION! 🔥     ║
║                                                              ║
║  Next Steps:                                                 ║
║  1. Run: python main.py                                      ║
║  2. Or use: python launch_phantom.py                         ║
║  3. Try voice command: "Phantom, system status"             ║
║  4. Explore the elite cyberpunk interface                   ║
║  5. Read README.md for advanced operations                   ║
║                                                              ║
║  🎭 Welcome to the digital underground, Agent! 🎭           ║
║                                                              ║
║  Remember: With great power comes great responsibility       ║
║  Use the Phantom Suite ethically and legally!               ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(completion_banner)
        print("👻 PHANTOM PROTOCOL ACTIVATED - ALL SYSTEMS OPERATIONAL 👻")
        print("\n🚨 WARNING: This is elite-level software. Use responsibly! 🚨")
    
    def run_setup(self):
        """Run the complete setup process"""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            print("❌ Critical error: Failed to install core dependencies")
            return False
        
        # Install optional packages
        self.install_optional_packages()
        
        # Create directories
        self.create_directories()
        
        # Create config files
        self.create_config_files()
        
        # Test installation
        self.test_installation()
        
        # Create launcher scripts
        self.create_launcher_scripts()
        
        # Generate setup report
        self.generate_setup_report()
        
        # Print completion message
        self.print_completion_message()
        
        return True

def main():
    """Main setup function"""
    setup = PhantomSetup()
    
    try:
        success = setup.run_setup()
        if success:
            print("\n🎯 Setup completed successfully!")
            return 0
        else:
            print("\n❌ Setup failed. Check the error messages above.")
            return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
