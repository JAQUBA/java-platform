# Universal Java Platform Builder for PlatformIO
import os
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
from os.path import join, exists, basename
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment

env = DefaultEnvironment()

# Configuration
JDK_VERSION = "18.0.2"
MAVEN_VERSION = "3.9.6"

def get_jdk_url():
    """Get JDK download URL based on platform"""
    system = platform.system().lower()
    arch = "x64" if platform.machine().lower() in ["x86_64", "amd64"] else "aarch64"
    
    if system == "windows":
        return f"https://download.oracle.com/java/18/archive/jdk-{JDK_VERSION}_windows-{arch}_bin.zip"
    elif system == "linux":
        return f"https://download.oracle.com/java/18/archive/jdk-{JDK_VERSION}_linux-{arch}_bin.tar.gz"
    elif system == "darwin":
        return f"https://download.oracle.com/java/18/archive/jdk-{JDK_VERSION}_macos-{arch}_bin.tar.gz"

def get_maven_url():
    """Get Maven download URL"""
    return f"https://archive.apache.org/dist/maven/maven-3/{MAVEN_VERSION}/binaries/apache-maven-{MAVEN_VERSION}-bin.zip"

def download_extract(url, dest_dir, extract_dir):
    """Download and extract archive"""
    os.makedirs(dest_dir, exist_ok=True)
    filename = basename(url)
    filepath = join(dest_dir, filename)
    
    if not exists(filepath):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
    
    if not exists(extract_dir):
        print(f"Extracting {filename}...")
        if filename.endswith('.zip'):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(dest_dir)
        else:
            with tarfile.open(filepath, 'r:gz') as tar_ref:
                tar_ref.extractall(dest_dir)

def install_jdk():
    """Install JDK 18"""
    platform_dir = env.PioPlatform().get_dir()
    packages_dir = join(platform_dir, "packages")
    downloads_dir = join(packages_dir, "downloads")
    jdk_dir = join(packages_dir, "toolchain-jdk18")
    
    if exists(jdk_dir):
        return jdk_dir
    
    url = get_jdk_url()
    download_extract(url, downloads_dir, packages_dir)
    
    # Find extracted JDK directory and rename it
    for item in os.listdir(packages_dir):
        if item.startswith("jdk-" + JDK_VERSION):
            os.rename(join(packages_dir, item), jdk_dir)
            break
    
    return jdk_dir

def install_maven():
    """Install Maven"""
    platform_dir = env.PioPlatform().get_dir()
    packages_dir = join(platform_dir, "packages")
    downloads_dir = join(packages_dir, "downloads")
    maven_dir = join(packages_dir, "tool-maven")
    
    if exists(maven_dir):
        return maven_dir
    
    url = get_maven_url()
    download_extract(url, downloads_dir, packages_dir)
    
    # Find extracted Maven directory and rename it
    for item in os.listdir(packages_dir):
        if item.startswith("apache-maven-" + MAVEN_VERSION):
            os.rename(join(packages_dir, item), maven_dir)
            break
    
    return maven_dir

def run_maven(target, project_dir, jdk_dir, maven_dir):
    """Run Maven command"""
    java_home = jdk_dir
    maven_cmd = join(maven_dir, "bin", "mvn.cmd" if platform.system() == "Windows" else "mvn")
    
    env_vars = os.environ.copy()
    env_vars["JAVA_HOME"] = java_home
    env_vars["PATH"] = f"{join(jdk_dir, 'bin')}{os.pathsep}{env_vars.get('PATH', '')}"
    
    cmd = [maven_cmd, target]
    result = subprocess.run(cmd, cwd=project_dir, env=env_vars, 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Maven error: {result.stderr}")
        raise Exception(f"Maven {target} failed")
    
    return result

# Install tools
jdk_path = install_jdk()
maven_path = install_maven()

# Set up environment
env.Replace(
    JAVA_HOME=jdk_path,
    MAVEN_HOME=maven_path,
)

# Build targets
def java_compile(target, source, env):
    """Compile Java project with Maven"""
    project_dir = env.get("PROJECT_DIR")
    run_maven("compile", project_dir, jdk_path, maven_path)
    return None

def java_package(target, source, env):
    """Package Java project with Maven"""
    project_dir = env.get("PROJECT_DIR")
    run_maven("package", project_dir, jdk_path, maven_path)
    return None

def java_test(target, source, env):
    """Run tests with Maven"""
    project_dir = env.get("PROJECT_DIR")
    run_maven("test", project_dir, jdk_path, maven_path)
    return None

def java_run(target, source, env):
    """Run Java application"""
    project_dir = env.get("PROJECT_DIR")
    jar_files = []
    
    # Find JAR files in target directory
    target_dir = join(project_dir, "target")
    if exists(target_dir):
        for file in os.listdir(target_dir):
            if file.endswith(".jar") and not file.endswith("-sources.jar"):
                jar_files.append(join(target_dir, file))
    
    if jar_files:
        java_exe = join(jdk_path, "bin", "java.exe" if platform.system() == "Windows" else "java")
        cmd = [java_exe, "-jar", jar_files[0]]
        subprocess.run(cmd, cwd=project_dir)
    else:
        print("No JAR file found to run")
    
    return None

# Register builders
env.Append(BUILDERS=dict(
    JavaCompile=Builder(action=java_compile),
    JavaPackage=Builder(action=java_package),
    JavaTest=Builder(action=java_test),
    JavaRun=Builder(action=java_run)
))

# Default targets
compile_target = env.JavaCompile("compile", [])
package_target = env.JavaPackage("package", compile_target)
test_target = env.JavaTest("test", compile_target)
run_target = env.JavaRun("run", package_target)

env.Alias("compile", compile_target)
env.Alias("package", package_target) 
env.Alias("test", test_target)
env.Alias("run", run_target)

Default(package_target)