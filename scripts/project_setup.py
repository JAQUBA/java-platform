import os
import sys
import json
import subprocess
from pathlib import Path

class ProjectSetup:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.src_dir = self.project_dir / "src" / "main" / "java"
        self.test_dir = self.project_dir / "src" / "test" / "java"
        self.resources_dir = self.project_dir / "src" / "main" / "resources"
        
    def create_maven_structure(self):
        """Create Maven project structure"""
        dirs_to_create = [
            self.src_dir,
            self.test_dir,
            self.resources_dir,
            self.project_dir / "src" / "test" / "resources"
        ]
        
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")
    
    def create_main_class(self, class_name="Main", package=None):
        """Create main Java class"""
        package_declaration = f"package {package};\n\n" if package else ""
        
        main_class_content = f"""{package_declaration}public class {class_name} {{
    public static void main(String[] args) {{
        System.out.println("Hello from PlatformIO Java Platform!");
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("Project ready for development!");
    }}
}}"""
        
        if package:
            package_dirs = package.split('.')
            class_dir = self.src_dir
            for pkg_dir in package_dirs:
                class_dir = class_dir / pkg_dir
            class_dir.mkdir(parents=True, exist_ok=True)
        else:
            class_dir = self.src_dir
        
        class_file = class_dir / f"{class_name}.java"
        with open(class_file, 'w', encoding='utf-8') as f:
            f.write(main_class_content)
        
        print(f"Created main class: {class_file}")
        return class_file
    
    def create_gitignore(self):
        """Create .gitignore for Java project"""
        gitignore_content = """# Compiled class files
*.class

# Log files
*.log

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# PlatformIO
.pio/
.vscode/.browse.c_cpp.db*
.vscode/c_cpp_properties.json
.vscode/launch.json
.vscode/ipch

# IDE
.idea/
*.iml
*.ipr
*.iws
.project
.classpath
.settings/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# JDK and Maven downloads
downloads/
packages/
"""
        
        gitignore_file = self.project_dir / ".gitignore"
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        print(f"Created .gitignore: {gitignore_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python project_setup.py <project_directory> [class_name] [package]")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    class_name = sys.argv[2] if len(sys.argv) > 2 else "Main"
    package = sys.argv[3] if len(sys.argv) > 3 else None
    
    setup = ProjectSetup(project_dir)
    
    print(f"Setting up Java project in: {project_dir}")
    
    # Create Maven structure
    setup.create_maven_structure()
    
    # Create main class
    setup.create_main_class(class_name, package)
    
    # Create .gitignore
    setup.create_gitignore()
    
    print("Project setup completed successfully!")

if __name__ == "__main__":
    main()
