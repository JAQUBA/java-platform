import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
import subprocess
from pathlib import Path

class JDKInstaller:
    def __init__(self, version="18.0.2"):
        self.version = version
        self.platform_name = platform.system().lower()
        self.arch = self._get_architecture()
        
    def _get_architecture(self):
        """Get system architecture"""
        arch = platform.machine().lower()
        if "x86_64" in arch or "amd64" in arch:
            return "x64"
        elif "aarch64" in arch or "arm64" in arch:
            return "aarch64"
        return arch
    
    def get_download_url(self):
        """Get JDK download URL based on platform"""
        base_url = "https://download.oracle.com/java/18/archive"
        
        if self.platform_name == "windows":
            return f"{base_url}/jdk-{self.version}_windows-{self.arch}_bin.zip"
        elif self.platform_name == "linux":
            return f"{base_url}/jdk-{self.version}_linux-{self.arch}_bin.tar.gz"
        elif self.platform_name == "darwin":
            return f"{base_url}/jdk-{self.version}_macos-{self.arch}_bin.tar.gz"
        else:
            raise ValueError(f"Unsupported platform: {self.platform_name}")
    
    def download_jdk(self, download_dir):
        """Download JDK archive"""
        url = self.get_download_url()
        filename = os.path.basename(url)
        filepath = os.path.join(download_dir, filename)
        
        if os.path.exists(filepath):
            print(f"JDK archive already exists: {filepath}")
            return filepath
        
        os.makedirs(download_dir, exist_ok=True)
        print(f"Downloading JDK from: {url}")
        
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"Downloaded: {filepath}")
            return filepath
        except Exception as e:
            print(f"Failed to download JDK: {e}")
            raise
    
    def extract_jdk(self, archive_path, extract_dir):
        """Extract JDK archive"""
        print(f"Extracting JDK to: {extract_dir}")
        os.makedirs(extract_dir, exist_ok=True)
        
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        elif archive_path.endswith('.tar.gz'):
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_dir)
        else:
            raise ValueError(f"Unsupported archive format: {archive_path}")
        
        # Find the extracted JDK directory
        for item in os.listdir(extract_dir):
            item_path = os.path.join(extract_dir, item)
            if os.path.isdir(item_path) and item.startswith('jdk'):
                return item_path
        
        raise RuntimeError("JDK directory not found after extraction")
    
    def install(self, install_dir):
        """Install JDK to specified directory"""
        java_exe = "java.exe" if self.platform_name == "windows" else "java"
        java_path = os.path.join(install_dir, "bin", java_exe)
        
        if os.path.exists(java_path):
            print(f"JDK already installed at: {install_dir}")
            return install_dir
        
        # Create temporary download directory
        download_dir = os.path.join(install_dir, "..", "downloads")
        
        try:
            # Download JDK
            archive_path = self.download_jdk(download_dir)
            
            # Extract JDK
            temp_extract_dir = os.path.join(download_dir, "extract")
            extracted_jdk_dir = self.extract_jdk(archive_path, temp_extract_dir)
            
            # Move to final location
            if os.path.exists(install_dir):
                import shutil
                shutil.rmtree(install_dir)
            
            import shutil
            shutil.move(extracted_jdk_dir, install_dir)
            
            # Cleanup
            shutil.rmtree(temp_extract_dir)
            
            print(f"JDK installed successfully at: {install_dir}")
            return install_dir
            
        except Exception as e:
            print(f"Failed to install JDK: {e}")
            raise
    
    def verify_installation(self, install_dir):
        """Verify JDK installation"""
        java_exe = "java.exe" if self.platform_name == "windows" else "java"
        java_path = os.path.join(install_dir, "bin", java_exe)
        
        if not os.path.exists(java_path):
            return False
        
        try:
            result = subprocess.run([java_path, "-version"], 
                                 capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

if __name__ == "__main__":
    installer = JDKInstaller()
    install_path = sys.argv[1] if len(sys.argv) > 1 else "./jdk18"
    
    try:
        installer.install(install_path)
        if installer.verify_installation(install_path):
            print("JDK installation verified successfully!")
        else:
            print("JDK installation verification failed!")
            sys.exit(1)
    except Exception as e:
        print(f"Installation failed: {e}")
        sys.exit(1)
