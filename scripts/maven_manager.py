import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

class MavenManager:
    def __init__(self, maven_home=None):
        self.maven_home = maven_home or self._find_maven()
        self.maven_cmd = self._get_maven_command()
    
    def _find_maven(self):
        """Find Maven installation"""
        # Check environment variable
        maven_home = os.environ.get('MAVEN_HOME')
        if maven_home and os.path.exists(maven_home):
            return maven_home
        
        # Check common locations
        common_paths = [
            "/usr/share/maven",
            "/opt/maven",
            "C:\\Program Files\\Apache\\Maven",
            "C:\\apache-maven"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _get_maven_command(self):
        """Get Maven command based on platform"""
        if not self.maven_home:
            return "mvn"  # Try system PATH
        
        if os.name == 'nt':  # Windows
            return os.path.join(self.maven_home, "bin", "mvn.cmd")
        else:
            return os.path.join(self.maven_home, "bin", "mvn")
    
    def parse_platformio_deps(self, lib_deps_string):
        """Parse PlatformIO lib_deps and convert to Maven dependencies"""
        dependencies = []
        
        for line in lib_deps_string.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse different formats:
            # 1. groupId:artifactId@version
            # 2. artifactId@version
            # 3. github_user/repo@version
            # 4. https://github.com/user/repo.git@version
            
            if '@' in line:
                dep_info, version = line.rsplit('@', 1)
            else:
                dep_info = line
                version = "LATEST"
            
            if ':' in dep_info:
                # Format: groupId:artifactId
                group_id, artifact_id = dep_info.split(':', 1)
            elif '/' in dep_info and not dep_info.startswith('http'):
                # Format: github_user/repo
                parts = dep_info.split('/')
                group_id = f"com.github.{parts[0]}"
                artifact_id = parts[1]
            elif dep_info.startswith('http'):
                # Git URL - extract repo name
                repo_name = dep_info.split('/')[-1].replace('.git', '')
                group_id = "com.github"
                artifact_id = repo_name
            else:
                # Single name - assume common library
                group_id = "org.apache.commons"
                artifact_id = dep_info
            
            dependencies.append({
                'groupId': group_id,
                'artifactId': artifact_id,
                'version': version
            })
        
        return dependencies
    
    def generate_pom_xml(self, project_dir, dependencies=None, project_name="java-project"):
        """Generate pom.xml file"""
        if dependencies is None:
            dependencies = []
        
        pom_template = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.platformio</groupId>
    <artifactId>{project_name}</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <properties>
        <maven.compiler.source>18</maven.compiler.source>
        <maven.compiler.target>18</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <dependencies>
{dependencies_xml}
    </dependencies>
    
    <build>
        <sourceDirectory>src/main/java</sourceDirectory>
        <testSourceDirectory>src/test/java</testSourceDirectory>
        
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>18</source>
                    <target>18</target>
                </configuration>
            </plugin>
            
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <archive>
                        <manifest>
                            <addClasspath>true</addClasspath>
                            <mainClass>Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
            
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-dependency-plugin</artifactId>
                <version>3.6.0</version>
                <executions>
                    <execution>
                        <id>copy-dependencies</id>
                        <phase>package</phase>
                        <goals>
                            <goal>copy-dependencies</goal>
                        </goals>
                        <configuration>
                            <outputDirectory>${{project.build.directory}}/lib</outputDirectory>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>'''
        
        # Generate dependencies XML
        dependencies_xml = ""
        for dep in dependencies:
            dependencies_xml += f'''        <dependency>
            <groupId>{dep['groupId']}</groupId>
            <artifactId>{dep['artifactId']}</artifactId>
            <version>{dep['version']}</version>
        </dependency>
'''
        
        pom_content = pom_template.format(
            project_name=project_name,
            dependencies_xml=dependencies_xml
        )
        
        pom_path = os.path.join(project_dir, "pom.xml")
        with open(pom_path, 'w', encoding='utf-8') as f:
            f.write(pom_content)
        
        print(f"Generated pom.xml at: {pom_path}")
        return pom_path
    
    def install_dependencies(self, project_dir):
        """Install Maven dependencies"""
        try:
            result = subprocess.run(
                [self.maven_cmd, "dependency:resolve"],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("Dependencies installed successfully")
                return True
            else:
                print(f"Failed to install dependencies: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            return False
    
    def compile_project(self, project_dir):
        """Compile Java project"""
        try:
            result = subprocess.run(
                [self.maven_cmd, "compile"],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("Project compiled successfully")
                return True
            else:
                print(f"Compilation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error compiling project: {e}")
            return False
    
    def package_project(self, project_dir):
        """Package Java project"""
        try:
            result = subprocess.run(
                [self.maven_cmd, "package"],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("Project packaged successfully")
                return True
            else:
                print(f"Packaging failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error packaging project: {e}")
            return False
    
    def run_project(self, project_dir, main_class="Main"):
        """Run Java project"""
        try:
            result = subprocess.run(
                [self.maven_cmd, "exec:java", f"-Dexec.mainClass={main_class}"],
                cwd=project_dir
            )
            
            return result.returncode == 0
                
        except Exception as e:
            print(f"Error running project: {e}")
            return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python maven_manager.py <command> <project_dir> [args...]")
        print("Commands: generate-pom, install, compile, package, run")
        sys.exit(1)
    
    command = sys.argv[1]
    project_dir = sys.argv[2]
    
    manager = MavenManager()
    
    if command == "generate-pom":
        lib_deps = sys.argv[3] if len(sys.argv) > 3 else ""
        dependencies = manager.parse_platformio_deps(lib_deps)
        manager.generate_pom_xml(project_dir, dependencies)
    
    elif command == "install":
        manager.install_dependencies(project_dir)
    
    elif command == "compile":
        manager.compile_project(project_dir)
    
    elif command == "package":
        manager.package_project(project_dir)
    
    elif command == "run":
        main_class = sys.argv[3] if len(sys.argv) > 3 else "Main"
        manager.run_project(project_dir, main_class)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
