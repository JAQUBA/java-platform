@echo off
REM Test script for PlatformIO Java Platform on Windows

echo ========================================
echo Testing PlatformIO Java Platform
echo ========================================

echo.
echo 1. Checking PlatformIO installation...
pio --version
if %ERRORLEVEL% neq 0 (
    echo ERROR: PlatformIO not found!
    echo Please install PlatformIO first.
    exit /b 1
)

echo.
echo 2. Checking platform installation...
pio platform list | findstr java-platform
if %ERRORLEVEL% neq 0 (
    echo ERROR: Java platform not installed!
    echo Please run install.py first.
    exit /b 1
)

echo.
echo 3. Building example project...
cd examples\basic-java
if not exist platformio.ini (
    echo ERROR: Example project not found!
    exit /b 1
)

echo.
echo 4. Running compilation...
pio run
if %ERRORLEVEL% neq 0 (
    echo ERROR: Compilation failed!
    exit /b 1
)

echo.
echo 5. Running packaging...
pio run -t upload
if %ERRORLEVEL% neq 0 (
    echo ERROR: Packaging failed!
    exit /b 1
)

echo.
echo ========================================
echo All tests passed successfully!
echo ========================================

echo.
echo Generated files:
if exist pom.xml echo - pom.xml (Maven configuration)
if exist target\*.jar echo - JAR file in target directory

echo.
echo To run the application:
echo java -jar target\*.jar

pause
