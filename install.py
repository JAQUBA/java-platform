#!/usr/bin/env python3
"""
PlatformIO Java Platform Installer

This script installs the Java platform for PlatformIO with automatic JDK 18 
and Maven dependency management.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def get_platformio_platforms_dir():
    """Get PlatformIO platforms directory"""
    if os.name == 'nt':  # Windows
        home_dir = os.environ.get('USERPROFILE', os.path.expanduser('~'))
    else:  # Linux/macOS
        home_dir = os.path.expanduser('~')
    
    platforms_dir = os.path.join(home_dir, '.platformio', 'platforms')
    return platforms_dir

def check_platformio_installed():
    """Check if PlatformIO is installed"""
    try:
        result = subprocess.run(['pio', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_platform(source_dir, force=False):
    """Install Java platform to PlatformIO"""
    platforms_dir = get_platformio_platforms_dir()
    target_dir = os.path.join(platforms_dir, 'java-platform')
    
    print(f"📦 Installing Java Platform...")
    print(f"📂 Source: {source_dir}")
    print(f"📍 Target: {target_dir}")
    
    # Check if platform already exists
    if os.path.exists(target_dir):
        if not force:
            response = input("Platform already exists. Overwrite? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("❌ Installation cancelled.")
                return False
        
        print("🗑️  Removing existing platform...")
        shutil.rmtree(target_dir)
    
    # Create platforms directory if it doesn't exist
    os.makedirs(platforms_dir, exist_ok=True)
    
    # Copy platform files
    print("📋 Copying platform files...")
    shutil.copytree(source_dir, target_dir)
    
    print("✅ Java Platform installed successfully!")
    return True

def test_platform():
    """Test platform installation"""
    print("🧪 Testing platform installation...")
    
    try:
        result = subprocess.run(['pio', 'platform', 'list'], 
                              capture_output=True, text=True)
        
        if 'java-platform' in result.stdout:
            print("✅ Platform registered successfully!")
            return True
        else:
            print("❌ Platform not found in PlatformIO list.")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_test_project():
    """Create a test project to verify installation"""
    test_dir = "test-java-project"
    
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    print(f"🧪 Creating test project: {test_dir}")
    
    try:
        # Initialize project
        result = subprocess.run([
            'pio', 'project', 'init', 
            '--board', 'generic',
            '--project-dir', test_dir
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to create test project: {result.stderr}")
            return False
        
        # Create platformio.ini
        platformio_ini = f"""[env:generic]
platform = java-platform
board = generic
framework = java

lib_deps = 
    org.slf4j:slf4j-api@2.0.7
    org.slf4j:slf4j-simple@2.0.7
"""
        
        with open(os.path.join(test_dir, 'platformio.ini'), 'w') as f:
            f.write(platformio_ini)
        
        # Create source structure
        src_dir = os.path.join(test_dir, 'src', 'main', 'java')
        os.makedirs(src_dir, exist_ok=True)
        
        # Create Main.java
        main_java = """import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    
    public static void main(String[] args) {
        logger.info("Hello from PlatformIO Java Platform!");
        logger.info("Java Version: " + System.getProperty("java.version"));
        logger.info("Test project working correctly!");
    }
}"""
        
        with open(os.path.join(src_dir, 'Main.java'), 'w') as f:
            f.write(main_java)
        
        print("✅ Test project created successfully!")
        print(f"📁 Project location: {os.path.abspath(test_dir)}")
        print("\n🚀 To test the platform, run:")
        print(f"   cd {test_dir}")
        print("   pio run")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test project: {e}")
        return False

def main():
    """Main installer function"""
    print("🔧 PlatformIO Java Platform Installer")
    print("=" * 50)
    
    # Check if PlatformIO is installed
    if not check_platformio_installed():
        print("❌ PlatformIO not found!")
        print("Please install PlatformIO first:")
        print("  pip install platformio")
        print("or visit: https://platformio.org/install")
        sys.exit(1)
    
    print("✅ PlatformIO found!")
    
    # Get source directory (current directory)
    source_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if we're in the right directory
    required_files = ['platform.json', 'platform.py', 'builder']
    for file in required_files:
        if not os.path.exists(os.path.join(source_dir, file)):
            print(f"❌ Required file/directory not found: {file}")
            print("Please run this script from the java-platform directory.")
            sys.exit(1)
    
    # Parse command line arguments
    force = '--force' in sys.argv or '-f' in sys.argv
    test_only = '--test' in sys.argv
    create_test = '--create-test' in sys.argv
    
    if test_only:
        success = test_platform()
        sys.exit(0 if success else 1)
    
    if create_test:
        success = create_test_project()
        sys.exit(0 if success else 1)
    
    # Install platform
    success = install_platform(source_dir, force)
    
    if success:
        # Test installation
        if test_platform():
            print("\n🎉 Installation completed successfully!")
            print("\nNext steps:")
            print("1. Create a new project:")
            print("   pio project init --board generic --platform java-platform")
            print("2. Or create a test project:")
            print(f"   python {__file__} --create-test")
        else:
            print("⚠️  Installation completed but test failed.")
            print("Please check PlatformIO configuration.")
    else:
        print("❌ Installation failed.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("PlatformIO Java Platform Installer")
        print("\nUsage:")
        print("  python install.py [options]")
        print("\nOptions:")
        print("  --force, -f      Force overwrite existing installation")
        print("  --test           Test existing installation")
        print("  --create-test    Create a test project")
        print("  --help, -h       Show this help message")
        sys.exit(0)
    
    main()
