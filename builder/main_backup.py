import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
from os.path import join, exists, dirname, basename
from platformio.builder.tools.piolib import ProjectAsLibBuilder
from platformio.package.manager.platform import PlatformPackageManager
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment

env = DefaultEnvironment()
platform_obj = env.PioPlatform()

# JDK 18 configuration
JDK_VERSION = "18.0.2"
MAVEN_VERSION = "3.9.6"

def get_jdk_download_url():
    """Get JDK download URL based on platform"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if "x86_64" in arch or "amd64" in arch:
        arch = "x64"
    elif "aarch64" in arch or "arm64" in arch:
        arch = "aarch64"
    
    if system == "windows":
        return f"https://download.oracle.com/java/18/archive/jdk-{JDK_VERSION}_windows-{arch}_bin.zip"
    elif system == "linux":
        return f"https://download.oracle.com/java/18/archive/jdk-{JDK_VERSION}_linux-{arch}_bin.tar.gz"
    elif system == "darwin":
        return f"https://download.oracle.com/java/18/archive/jdk-{JDK_VERSION}_macos-{arch}_bin.tar.gz"

def get_maven_download_url():
    """Get Maven download URL"""
    return f"https://archive.apache.org/dist/maven/maven-3/{MAVEN_VERSION}/binaries/apache-maven-{MAVEN_VERSION}-bin.zip"

def download_and_extract(url, dest_dir, extract_dir):
    """Download and extract archive"""
    if not exists(dest_dir):
        os.makedirs(dest_dir)
    
    filename = basename(url)
    filepath = join(dest_dir, filename)
    
    if not exists(filepath):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
    
    print(f"Extracting {filename}...")
    if filename.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    elif filename.endswith('.tar.gz'):
        with tarfile.open(filepath, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_dir)

def install_jdk():
    """Install JDK 18"""
    packages_dir = join(platform_obj.get_dir(), "packages")
    jdk_dir = join(packages_dir, "toolchain-jdk18")
    
    if exists(join(jdk_dir, "bin", "java" + (".exe" if platform.system() == "Windows" else ""))):
        print("JDK 18 already installed")
        return jdk_dir
    
    print("Installing JDK 18...")
    jdk_url = get_jdk_download_url()
    download_dir = join(packages_dir, "downloads")
    
    download_and_extract(jdk_url, download_dir, packages_dir)
    
    # Find extracted JDK directory and rename it
    for item in os.listdir(packages_dir):
        if item.startswith("jdk-18") and os.path.isdir(join(packages_dir, item)):
            old_path = join(packages_dir, item)
            if old_path != jdk_dir:
                if exists(jdk_dir):
                    import shutil
                    shutil.rmtree(jdk_dir)
                os.rename(old_path, jdk_dir)
            break
    
    return jdk_dir

def install_maven():
    """Install Maven"""
    packages_dir = join(platform_obj.get_dir(), "packages")
    maven_dir = join(packages_dir, "tool-maven")
    
    if exists(join(maven_dir, "bin", "mvn" + (".cmd" if platform.system() == "Windows" else ""))):
        print("Maven already installed")
        return maven_dir
    
    print("Installing Maven...")
    maven_url = get_maven_download_url()
    download_dir = join(packages_dir, "downloads")
    
    download_and_extract(maven_url, download_dir, packages_dir)
    
    # Find extracted Maven directory and rename it
    for item in os.listdir(packages_dir):
        if item.startswith("apache-maven-") and os.path.isdir(join(packages_dir, item)):
            old_path = join(packages_dir, item)
            if old_path != maven_dir:
                if exists(maven_dir):
                    import shutil
                    shutil.rmtree(maven_dir)
                os.rename(old_path, maven_dir)
            break
    
    return maven_dir

def parse_lib_deps():
    """Parse maven_dependencies from platformio.ini and convert to Maven dependencies"""
    project_config = env.GetProjectConfig()
    env_section = "env:" + env.get("PIOENV", "generic")  # Default to 'generic'
    
    print(f"🔍 DEBUG: Looking for dependencies in section: {env_section}")
    
    # Debug: List all available sections and options
    print(f"🔍 DEBUG: Available sections: {project_config.sections()}")
    if project_config.has_section(env_section):
        print(f"🔍 DEBUG: Available options in {env_section}: {project_config.options(env_section)}")
    
    # Try maven_dependencies first, fallback to lib_deps for compatibility
    maven_deps_str = ""
    try:
        if project_config.has_option(env_section, "maven_dependencies"):
            maven_deps_str = project_config.get(env_section, "maven_dependencies")
            print(f"🔍 DEBUG: Found maven_dependencies: {repr(maven_deps_str)}")
        elif project_config.has_option(env_section, "lib_deps"):
            maven_deps_str = project_config.get(env_section, "lib_deps")
            print(f"🔍 DEBUG: Found lib_deps: {repr(maven_deps_str)}")
        else:
            print(f"❌ DEBUG: Neither maven_dependencies nor lib_deps found in {env_section}")
    except Exception as e:
        print(f"❌ DEBUG: Error reading dependencies: {e}")
    
    maven_deps = []
    if maven_deps_str.strip():
        for dep in maven_deps_str.split('\n'):
            dep = dep.strip()
            if dep and not dep.startswith('#') and not dep.startswith(';'):
                print(f"🔍 DEBUG: Processing dependency: {repr(dep)}")
                # Support both formats: groupId:artifactId:version and groupId:artifactId@version
                if ':' in dep and dep.count(':') >= 2:
                    # Maven format: groupId:artifactId:version
                    parts = dep.split(':')
                    group_id = parts[0]
                    artifact_id = parts[1]
                    artifact_version = ':'.join(parts[2:])  # Handle versions with colons
                    print(f"✅ DEBUG: Parsed Maven format: {group_id}:{artifact_id}:{artifact_version}")
                elif '@' in dep:
                    # PlatformIO format: groupId:artifactId@version
                    parts = dep.split('@')
                    artifact_version = parts[1]
                    artifact_info = parts[0]
                    
                    if ':' in artifact_info:
                        group_id, artifact_id = artifact_info.split(':', 1)
                    else:
                        # Default group for common libraries
                        group_id = "org.apache.commons"
                        artifact_id = artifact_info
                    print(f"✅ DEBUG: Parsed PlatformIO format: {group_id}:{artifact_id}:{artifact_version}")
                else:
                    print(f"⚠️ DEBUG: Skipping invalid dependency format: {dep}")
                    continue  # Skip invalid dependencies
                
                maven_deps.append({
                    'groupId': group_id,
                    'artifactId': artifact_id,
                    'version': artifact_version
                })
    
    print(f"✅ DEBUG: Total parsed dependencies: {len(maven_deps)}")
    return maven_deps

def generate_pom_xml():
    """Generate pom.xml file with dependencies from maven_dependencies"""
    maven_deps = parse_lib_deps()
    project_config = env.GetProjectConfig()
    env_section = "env:" + env.get("PIOENV", "generic")  # Default to 'generic'
    
    # Debug: print what we found
    print(f"🔍 DEBUG: Found {len(maven_deps)} Maven dependencies:")
    for dep in maven_deps:
        print(f"   - {dep['groupId']}:{dep['artifactId']}:{dep['version']}")
    
    # ...existing code...
    
    # Get project information from platformio.ini
    try:
        project_name = project_config.get(env_section, "project_name", fallback="java-project")
    except:
        project_name = "java-project"
    
    try:
        project_version = project_config.get(env_section, "project_version", fallback="1.0.0")
    except:
        project_version = "1.0.0"
    
    try:
        project_description = project_config.get(env_section, "project_description", fallback="Java project built with PlatformIO")
    except:
        project_description = "Java project built with PlatformIO"
    
    try:
        extra_repositories = project_config.get(env_section, "extra_repositories", fallback="")
    except:
        extra_repositories = ""
    
    # Parse compiler source/target from build_flags
    compiler_source = "18"
    compiler_target = "18"
    try:
        build_flags = project_config.get(env_section, "build_flags", fallback="")
        for flag in build_flags.split('\n'):
            flag = flag.strip()
            if flag.startswith('-Dmaven.compiler.source='):
                compiler_source = flag.split('=')[1]
            elif flag.startswith('-Dmaven.compiler.target='):
                compiler_target = flag.split('=')[1]
    except:
        pass
    
    pom_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.platformio</groupId>
    <artifactId>{project_name}</artifactId>
    <version>{project_version}</version>
    <packaging>jar</packaging>
    
    <name>{project_name}</name>
    <description>{project_description}</description>
    
    <properties>
        <maven.compiler.source>{compiler_source}</maven.compiler.source>
        <maven.compiler.target>{compiler_target}</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>'''
    
    # Add repositories if specified
    if extra_repositories.strip():
        pom_content += '''
    
    <repositories>'''
        repos = [repo.strip() for repo in extra_repositories.split('\n') if repo.strip()]
        for i, repo in enumerate(repos):
            repo_id = f"repo{i+1}"
            pom_content += f'''
        <repository>
            <id>{repo_id}</id>
            <url>{repo}</url>
        </repository>'''
        pom_content += '''
    </repositories>'''
    
    pom_content += '''
    
    <dependencies>
'''
    
    for dep in maven_deps:
        pom_content += f'''        <dependency>
            <groupId>{dep['groupId']}</groupId>
            <artifactId>{dep['artifactId']}</artifactId>
            <version>{dep['version']}</version>
        </dependency>
'''
    
    pom_content += '''    </dependencies>
    
    <build>
        <sourceDirectory>src/main/java</sourceDirectory>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>''' + compiler_source + '''</source>
                    <target>''' + compiler_target + '''</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>'''
    
    with open(join(env.get("PROJECT_DIR"), "pom.xml"), 'w') as f:
        f.write(pom_content)

def ensure_project_structure(project_dir):
    """Ensure Maven project structure exists"""
    required_dirs = [
        "src/main/java",
        "src/main/resources",
        "src/test/java",
        "src/test/resources"
    ]
    
    for dir_path in required_dirs:
        full_path = join(project_dir, dir_path)
        if not exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            print(f"📁 Created directory: {dir_path}")

def java_compile_action(target, source, env):
    """Compile Java sources using Maven"""
    project_dir = env.get("PROJECT_DIR")
    
    try:
        # Ensure project structure exists
        ensure_project_structure(project_dir)
        
        maven_dir = install_maven()
        jdk_dir = install_jdk()
        
        # Set JAVA_HOME and PATH
        env_vars = os.environ.copy()
        env_vars["JAVA_HOME"] = jdk_dir
        env_vars["PATH"] = join(jdk_dir, "bin") + os.pathsep + env_vars.get("PATH", "")
        env_vars["MAVEN_HOME"] = maven_dir
        
        # Generate pom.xml from lib_deps
        generate_pom_xml()
        
        # Run Maven compile
        maven_cmd = join(maven_dir, "bin", "mvn" + (".cmd" if platform.system() == "Windows" else ""))
        cmd = [maven_cmd, "clean", "compile"]
        
        print(f"🔨 Compiling Java project...")
        print(f"📁 Project directory: {project_dir}")
        print(f"☕ Using JDK: {jdk_dir}")
        print(f"📦 Using Maven: {maven_dir}")
        print(f"🚀 Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=project_dir, env=env_vars, 
                              capture_output=False, text=True)
        
        if result.returncode != 0:
            print("❌ Maven compilation failed!")
            sys.exit(1)
        else:
            print("✅ Compilation successful!")
        
    except Exception as e:
        print(f"❌ Compilation error: {e}")
        sys.exit(1)
    
    return None

def java_package_action(target, source, env):
    """Package Java application using Maven"""
    project_dir = env.get("PROJECT_DIR")
    
    try:
        maven_dir = install_maven()
        jdk_dir = install_jdk()
        
        # Set JAVA_HOME and PATH
        env_vars = os.environ.copy()
        env_vars["JAVA_HOME"] = jdk_dir
        env_vars["PATH"] = join(jdk_dir, "bin") + os.pathsep + env_vars.get("PATH", "")
        env_vars["MAVEN_HOME"] = maven_dir
        
        # Run Maven package
        maven_cmd = join(maven_dir, "bin", "mvn" + (".cmd" if platform.system() == "Windows" else ""))
        cmd = [maven_cmd, "package", "-DskipTests"]
        
        print(f"📦 Packaging Java project...")
        print(f"📁 Project directory: {project_dir}")
        print(f"🚀 Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=project_dir, env=env_vars, 
                              capture_output=False, text=True)
        
        if result.returncode != 0:
            print("❌ Maven packaging failed!")
            sys.exit(1)
        else:
            print("✅ Packaging successful!")
            
            # Find generated JAR file
            target_dir = join(project_dir, "target")
            if exists(target_dir):
                jar_files = [f for f in os.listdir(target_dir) if f.endswith('.jar')]
                if jar_files:
                    print(f"📦 Generated JAR: {jar_files[0]}")
                    print(f"📍 Location: {join(target_dir, jar_files[0])}")
        
    except Exception as e:
        print(f"❌ Packaging error: {e}")
        sys.exit(1)
    
    return None

# Install JDK and Maven
jdk_path = install_jdk()
maven_path = install_maven()

# Configure environment
env.Replace(
    AR="jar",
    CC=join(jdk_path, "bin", "javac" + (".exe" if platform.system() == "Windows" else "")),
    CXX=join(jdk_path, "bin", "javac" + (".exe" if platform.system() == "Windows" else "")),
    RANLIB="echo",
    JAVA_HOME=jdk_path,
    MAVEN_HOME=maven_path
)

# Add JDK and Maven to PATH
env.PrependENVPath("PATH", join(jdk_path, "bin"))
env.PrependENVPath("PATH", join(maven_path, "bin"))

# Define builders
env.Append(
    BUILDERS=dict(
        JavaCompile=Builder(action=java_compile_action),
        JavaPackage=Builder(action=java_package_action)
    )
)

# Define targets
compile_target = env.JavaCompile("$BUILD_DIR/compile.timestamp", None)
package_target = env.JavaPackage("$BUILD_DIR/package.timestamp", compile_target)

# Set default target
Default(package_target)

# Always build
AlwaysBuild(compile_target)
AlwaysBuild(package_target)
