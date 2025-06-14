import os
import sys
from platformio.platform.base import PlatformBase
from platformio.util import get_systype

class JavaplatformPlatform(PlatformBase):
    def __init__(self, manifest_path):
        super().__init__(manifest_path)
        self.jdk_version = "18"
        self.maven_version = "3.9.6"
    
    def configure_default_packages(self, variables, targets):
        packages = super().configure_default_packages(variables, targets)
        
        # Ensure Java framework is available
        if "framework-java" not in packages:
            packages["framework-java"] = {}
        
        # Ensure JDK 18 is installed
        if "toolchain-jdk18" not in packages:
            packages["toolchain-jdk18"] = {}
            
        # Ensure Maven is installed
        if "tool-maven" not in packages:
            packages["tool-maven"] = {}
            
        return packages
    
    def get_boards(self, id_=None):
        result = super().get_boards(id_)
        if not result:
            result = {}
        return result
    
    def configure_debug_session(self, debug_config):
        return debug_config
    
    def on_installed(self):
        """Called after platform installation"""
        self._install_jdk18()
        self._install_maven()
    
    def _install_jdk18(self):
        """Install JDK 18 if not present"""
        jdk_path = self._get_jdk_path()
        if not os.path.exists(jdk_path):
            print("Installing JDK 18...")
            # JDK installation will be handled by package manager
    
    def _install_maven(self):
        """Install Maven if not present"""
        maven_path = self._get_maven_path()
        if not os.path.exists(maven_path):
            print("Installing Maven...")
            # Maven installation will be handled by package manager
    
    def _get_jdk_path(self):
        """Get JDK installation path"""
        return os.path.join(self.get_dir(), "packages", "toolchain-jdk18")
    
    def _get_maven_path(self):
        """Get Maven installation path"""
        return os.path.join(self.get_dir(), "packages", "tool-maven")
