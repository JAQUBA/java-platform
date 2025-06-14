# PlatformIO Java Platform

🚀 **Platforma PlatformIO dla rozwoju aplikacji Java z automatycznym pobieraniem JDK 18 i zarządzaniem zależnościami Maven**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-6.0%2B-orange)](https://platformio.org/)
[![Java](https://img.shields.io/badge/Java-18-blue)](https://openjdk.java.net/projects/jdk/18/)
[![Maven](https://img.shields.io/badge/Maven-3.9.6-red)](https://maven.apache.org/)

## ✨ Funkcje

- 🔄 **Automatyczne pobieranie JDK 18** - Platforma automatycznie pobiera i instaluje JDK 18.0.2
- 📦 **Zarządzanie zależnościami Maven** - Zależności z `lib_deps` są automatycznie konwertowane do pom.xml
- 🏗️ **Integracja z PlatformIO** - Pełna integracja z workflow PlatformIO (`pio run`, `pio run -t upload`)
- 🌍 **Wsparcie wieloplatformowe** - Windows, Linux, macOS (x64, ARM64)
- 📋 **Inteligentne parsowanie** - Obsługa różnych formatów zależności
- 🧪 **Gotowe przykłady** - Przykładowy projekt z popularnymi bibliotekami

## 🚀 Szybki start

### 1. Instalacja

```bash
# Sklonuj lub pobierz platformę
git clone https://github.com/your-repo/platformio-java-platform.git
cd platformio-java-platform

# Zainstaluj platformę
python install.py
```

### 2. Stwórz projekt

```bash
# Inicjalizuj nowy projekt
mkdir moj-projekt-java
cd moj-projekt-java
pio project init --board generic --platform java-platform
```

### 3. Konfiguruj zależności

```ini
# platformio.ini
[env:generic]
platform = java-platform
board = generic
framework = java

lib_deps = 
    org.apache.commons:commons-lang3@3.12.0
    org.slf4j:slf4j-api@2.0.7
    org.slf4j:slf4j-simple@2.0.7
```

### 4. Napisz kod

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
        logger.info("Message: {}", message);
        logger.info("Reversed: {}", StringUtils.reverse(message));
    }
}
```

### 5. Kompiluj i uruchom

```bash
# Kompilacja
pio run

# Packaging
pio run -t upload

# Uruchomienie
java -jar target/*.jar
```

## 📋 Obsługiwane formaty zależności

| Format | Przykład | Opis |
|--------|----------|------|
| **Maven pełny** | `org.apache.commons:commons-lang3@3.12.0` | Pełny Maven coordinates |
| **Maven skrócony** | `commons-lang3@3.12.0` | Automatyczny groupId |
| **GitHub** | `google/gson@2.10.1` | GitHub user/repo |
| **Git URL** | `https://github.com/user/repo.git@tag` | Pełny URL Git |

## 🛠️ Wymagania

- **PlatformIO Core** 6.0+
- **Python** 3.7+
- **Miejsce na dysku** ~500MB (JDK + Maven + cache)
- **Internet** (pierwsza instalacja)

## 📚 Dokumentacja

- **[Instrukcja użytkowania](USAGE.md)** - Szczegółowy przewodnik
- **[Changelog](CHANGELOG.md)** - Historia zmian
- **[Przykład](examples/basic-java/)** - Kompletny przykład projektu

## 🧪 Testowanie

```bash
# Test platformy
python install.py --test

# Stwórz projekt testowy
python install.py --create-test

# Test na Windows
test.bat

# Test na Linux/macOS
./test.sh
```

## 🔧 Zaawansowane użycie

### Własne targety

```ini
[env:generic]
platform = java-platform
board = generic
framework = java

# Własny target kompilacji
upload_command = mvn clean compile exec:java -Dexec.mainClass="Main"
```

### Debugowanie

```ini
[env:generic]
platform = java-platform
board = generic
framework = java

debug_tool = jdb
debug_port = 5005
```

## 📦 Popularne biblioteki

```ini
lib_deps = 
    # Logging
    org.slf4j:slf4j-api@2.0.7
    ch.qos.logback:logback-classic@1.4.7
    
    # Apache Commons
    org.apache.commons:commons-lang3@3.12.0
    org.apache.commons:commons-collections4@4.4
    
    # JSON
    com.fasterxml.jackson.core:jackson-core@2.15.0
    com.google.code.gson:gson@2.10.1
    
    # HTTP
    org.apache.httpcomponents:httpclient@4.5.14
    
    # Testing
    org.junit.jupiter:junit-jupiter@5.9.2
```

## 🏗️ Struktura platformy

```
java-platform/
├── platform.json              # Konfiguracja platformy PlatformIO
├── platform.py               # Logika platformy Python
├── builder/
│   └── main.py               # Builder SCons
├── boards/
│   └── generic.json          # Konfiguracja board
├── scripts/
│   ├── jdk_installer.py      # Installer JDK
│   ├── maven_manager.py      # Manager Maven
│   └── project_setup.py      # Setup projektu
├── examples/
│   └── basic-java/           # Przykładowy projekt
└── install.py               # Installer platformy
```

## ❓ Rozwiązywanie problemów

### JDK nie zostaje pobrany
```bash
# Wyczyść i zainstaluj ponownie
python install.py --force

# Ręczna instalacja
python scripts/jdk_installer.py ~/.platformio/platforms/java-platform/packages/toolchain-jdk18
```

### Błędy Maven
```bash
# Sprawdź pom.xml
cat pom.xml

# Wyczyść cache Maven
mvn clean
```

### Problemy z kompilacją
```bash
# Sprawdź strukturę
tree src/

# Stwórz strukturę Maven
python scripts/project_setup.py .
```

## 🤝 Wkład w rozwój

1. Fork projektu
2. Stwórz branch funkcjonalności (`git checkout -b feature/AmazingFeature`)
3. Commit zmian (`git commit -m 'Add some AmazingFeature'`)
4. Push branch (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📄 Licencja

Rozpowszechniane na licencji MIT. Zobacz [LICENSE](LICENSE) dla szczegółów.

## 🙏 Podziękowania

- [PlatformIO](https://platformio.org/) za fantastyczny framework
- [Oracle](https://www.oracle.com/) za JDK
- [Apache Software Foundation](https://www.apache.org/) za Maven
- Społeczność Java za niesamowite biblioteki open source

## 📞 Wsparcie

- **Issues**: [GitHub Issues](https://github.com/your-repo/platformio-java/issues)
- **Dyskusje**: [GitHub Discussions](https://github.com/your-repo/platformio-java/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/your-repo/platformio-java/wiki)

---

<p align="center">
  <strong>Zrobione z ❤️ dla społeczności Java i PlatformIO</strong>
</p>
