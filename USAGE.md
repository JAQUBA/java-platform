# Instrukcja użytkowania PlatformIO Java Platform

## Instalacja

### 1. Wymagania wstępne
- PlatformIO Core 6.0+
- Python 3.7+
- Połączenie internetowe (do pobierania JDK i Maven)
- ~500MB wolnego miejsca na dysku

### 2. Instalacja PlatformIO (jeśli nie jest zainstalowane)
```bash
# Przez pip
pip install platformio

# Lub przez conda
conda install -c conda-forge platformio
```

### 3. Instalacja platformy Java
```bash
# Z tego repozytorium
cd java-platform
python install.py

# Lub z opcją force (nadpisanie istniejącej instalacji)
python install.py --force
```

### 4. Weryfikacja instalacji
```bash
# Test platformy
python install.py --test

# Stworzenie projektu testowego
python install.py --create-test
```

## Tworzenie projektu

### 1. Inicjalizacja nowego projektu
```bash
# Stwórz nowy folder
mkdir moj-projekt-java
cd moj-projekt-java

# Inicjalizuj projekt PlatformIO
pio project init --board generic --platform java-platform
```

### 2. Konfiguracja platformio.ini
```ini
[env:generic]
platform = java-platform
board = generic
framework = java

# Zależności Maven
lib_deps = 
    org.apache.commons:commons-lang3@3.12.0
    org.slf4j:slf4j-api@2.0.7
    org.slf4j:slf4j-simple@2.0.7

# Opcje kompilacji (opcjonalne)
build_flags = 
    -Dmaven.compiler.source=18
    -Dmaven.compiler.target=18

# Ustawienia upload/packaging
upload_protocol = custom
upload_command = mvn package
```

### 3. Struktura projektu
Utwórz strukturę katalogów Maven:
```
moj-projekt/
├── src/
│   ├── main/
│   │   ├── java/          # Kod źródłowy
│   │   └── resources/     # Zasoby
│   └── test/
│       ├── java/          # Testy
│       └── resources/
└── platformio.ini
```

### 4. Przykładowa klasa Main.java
```java
// src/main/java/Main.java
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    
    public static void main(String[] args) {
        logger.info("Hello from PlatformIO Java Platform!");
        
        String message = "PlatformIO + Java = ❤️";
        String reversed = StringUtils.reverse(message);
        
        logger.info("Original: {}", message);
        logger.info("Reversed: {}", reversed);
        logger.info("Java Version: {}", System.getProperty("java.version"));
    }
}
```

## Kompilacja i uruchamianie

### 1. Kompilacja
```bash
# Kompiluj projekt
pio run

# Kompiluj z verbose output
pio run -v
```

### 2. Packaging (tworzenie JAR)
```bash
# Stwórz JAR
pio run -t upload

# Lub bezpośrednio Maven
mvn package
```

### 3. Uruchomienie
```bash
# Uruchom skompilowaną aplikację
java -jar target/*.jar

# Lub z określonym JAR
java -jar target/java-project-1.0.0.jar
```

## Zarządzanie zależnościami

### Formaty lib_deps

#### 1. Format Maven (zalecany)
```ini
lib_deps = 
    org.apache.commons:commons-lang3@3.12.0
    org.slf4j:slf4j-api@2.0.7
    com.fasterxml.jackson.core:jackson-core@2.15.0
```

#### 2. Format skrócony
```ini
lib_deps = 
    commons-lang3@3.12.0        # groupId: org.apache.commons
    slf4j-api@2.0.7             # groupId: org.slf4j
```

#### 3. GitHub dependencies
```ini
lib_deps = 
    google/gson@2.10.1
    FasterXML/jackson-core@2.15.0
```

### Popularne biblioteki Java
```ini
lib_deps = 
    # Logging
    org.slf4j:slf4j-api@2.0.7
    org.slf4j:slf4j-simple@2.0.7
    
    # Apache Commons
    org.apache.commons:commons-lang3@3.12.0
    org.apache.commons:commons-collections4@4.4
    org.apache.commons:commons-io@2.11.0
    
    # JSON
    com.fasterxml.jackson.core:jackson-core@2.15.0
    com.google.code.gson:gson@2.10.1
    
    # HTTP Client
    org.apache.httpcomponents:httpclient@4.5.14
    
    # Testing
    org.junit.jupiter:junit-jupiter@5.9.2
    org.mockito:mockito-core@5.1.1
```

## Debugowanie

### 1. Konfiguracja debugowania
```ini
[env:generic]
platform = java-platform
board = generic
framework = java

debug_tool = jdb
debug_port = 5005
```

### 2. Uruchomienie z debugowaniem
```bash
# Debug session
pio debug

# Lub ręcznie
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 -jar target/*.jar
```

## Rozwiązywanie problemów

### Problem: JDK nie zostaje pobrany
```bash
# Sprawdź logi
pio run -v

# Wyczyść cache i spróbuj ponownie
python install.py --force

# Ręczna instalacja JDK
python scripts/jdk_installer.py ~/.platformio/platforms/java-platform/packages/toolchain-jdk18
```

### Problem: Błędy Maven
```bash
# Sprawdź czy pom.xml został wygenerowany
ls pom.xml

# Ręczne wygenerowanie pom.xml
python scripts/maven_manager.py generate-pom . "org.slf4j:slf4j-api@2.0.7"

# Wyczyść cache Maven
mvn clean
mvn dependency:purge-local-repository
```

### Problem: Błędy kompilacji
```bash
# Sprawdź strukturę projektu
tree src/

# Stwórz strukturę Maven
python scripts/project_setup.py .

# Sprawdź Java syntax
javac src/main/java/*.java
```

### Problem: Problemy z platformą
```bash
# Reinstalacja platformy
pio platform uninstall java-platform
python install.py --force

# Test platformy
python install.py --test
```

## Zaawansowane użycie

### 1. Własne targety Maven
```ini
[env:generic]
platform = java-platform
board = generic
framework = java

# Własny target upload
upload_command = mvn clean compile package exec:java -Dexec.mainClass="Main"
```

### 2. Profile Maven
Dodaj do wygenerowanego pom.xml:
```xml
<profiles>
    <profile>
        <id>development</id>
        <properties>
            <maven.compiler.debug>true</maven.compiler.debug>
        </properties>
    </profile>
</profiles>
```

### 3. Packaging z zależnościami
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.6.0</version>
    <configuration>
        <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
        <archive>
            <manifest>
                <mainClass>Main</mainClass>
            </manifest>
        </archive>
    </configuration>
</plugin>
```

## Wsparcie

- **Issues**: [GitHub Issues](https://github.com/your-repo/platformio-java/issues)
- **Dokumentacja**: [GitHub Wiki](https://github.com/your-repo/platformio-java/wiki)
- **Dyskusje**: [GitHub Discussions](https://github.com/your-repo/platformio-java/discussions)

## Licencja

MIT License - Zobacz plik [LICENSE](LICENSE).
