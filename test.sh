#!/bin/bash
# Test script for PlatformIO Java Platform on Linux/macOS

echo "========================================"
echo "Testing PlatformIO Java Platform"
echo "========================================"

echo ""
echo "1. Checking PlatformIO installation..."
if ! command -v pio &> /dev/null; then
    echo "ERROR: PlatformIO not found!"
    echo "Please install PlatformIO first."
    exit 1
fi

pio --version

echo ""
echo "2. Checking platform installation..."
if ! pio platform list | grep -q java-platform; then
    echo "ERROR: Java platform not installed!"
    echo "Please run install.py first."
    exit 1
fi

echo ""
echo "3. Building example project..."
cd examples/basic-java || {
    echo "ERROR: Example project not found!"
    exit 1
}

if [ ! -f platformio.ini ]; then
    echo "ERROR: platformio.ini not found!"
    exit 1
fi

echo ""
echo "4. Running compilation..."
if ! pio run; then
    echo "ERROR: Compilation failed!"
    exit 1
fi

echo ""
echo "5. Running packaging..."
if ! pio run -t upload; then
    echo "ERROR: Packaging failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "All tests passed successfully!"
echo "========================================"

echo ""
echo "Generated files:"
[ -f pom.xml ] && echo "- pom.xml (Maven configuration)"
[ -f target/*.jar ] && echo "- JAR file in target directory"

echo ""
echo "To run the application:"
echo "java -jar target/*.jar"
