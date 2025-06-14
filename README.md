# Universal Java Platform Example

This example demonstrates how to use the Universal Java Platform for PlatformIO.

## Features
- Automatic JDK 18 installation
- Maven dependency management  
- Universal support for any Java project type
- Simple build and run process

## Usage

1. Create your Java project with standard Maven structure:
```
project/
├── platformio.ini
├── pom.xml
└── src/
    └── main/
        └── java/
            └── Main.java
```

2. Configure `platformio.ini`:
```ini
[env:java]
platform = /path/to/java-platform
board = generic
framework = java
```

3. Create your `pom.xml` with dependencies and build configuration

4. Build and run:
```bash
pio run          # Compile and package
pio run -t run   # Run the application
pio run -t test  # Run tests
```

## Project Types Supported
- Spring Boot applications
- Command-line tools
- Desktop applications (JavaFX, Swing)
- Minecraft plugins
- Enterprise applications
- Libraries and frameworks

The platform automatically handles Maven dependencies and build process.
