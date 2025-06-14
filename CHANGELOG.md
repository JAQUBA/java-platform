# Changelog

Wszystkie istotne zmiany w tym projekcie będą dokumentowane w tym pliku.

Format bazuje na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-14

### Dodane
- 🎉 Pierwsza wersja PlatformIO Java Platform
- ☕ Automatyczne pobieranie i instalacja JDK 18.0.2
- 📦 Automatyczne pobieranie i instalacja Apache Maven 3.9.6
- 🔄 Konwersja lib_deps z PlatformIO do formatu Maven
- 🏗️ Automatyczne generowanie pom.xml
- 🏛️ Wsparcie dla struktury projektu Maven
- 🖥️ Wsparcie dla Windows, Linux i macOS
- 🔧 Wsparcie dla architektur x64 i ARM64
- 🐛 Debugowanie z JDB
- 📚 Pełna dokumentacja i przykłady
- 🧪 Skrypty testowe i instalacyjne
- 📋 Przykładowy projekt z Apache Commons i SLF4J

### Funkcje techniczne
- Automatyczna detekcja platformy i architektury
- Cachowanie pobranych pakietów
- Inteligentne parsowanie zależności lib_deps
- Obsługa różnych formatów zależności (Maven, GitHub, skrócone)
- Tworzenie struktury katalogów Maven
- Integracja z workflow PlatformIO (pio run, pio run -t upload)
- Obsługa zmiennych środowiskowych
- Logowanie z emoji dla lepszej czytelności

### Obsługiwane formaty lib_deps
- `org.apache.commons:commons-lang3@3.12.0` (pełny format Maven)
- `commons-lang3@3.12.0` (format skrócony)
- `google/gson@2.10.1` (GitHub user/repo)
- `https://github.com/user/repo.git@version` (URL Git)

### Narzędzia
- `install.py` - Installer platformy z opcjami testowania
- `scripts/jdk_installer.py` - Standalone installer JDK 18
- `scripts/maven_manager.py` - Manager zależności Maven
- `scripts/project_setup.py` - Generator struktury projektu
- `test.bat` / `test.sh` - Skrypty testowe dla różnych platform

### Dokumentacja
- `README.md` - Główna dokumentacja platformy
- `USAGE.md` - Szczegółowa instrukcja użytkowania
- `examples/basic-java/` - Przykładowy projekt z dokumentacją
- Inline komentarze w kodzie Python

### Konfiguracja
- `platform.json` - Definicja platformy PlatformIO
- `boards/generic.json` - Konfiguracja board generic
- `.env` - Zmienne środowiskowe i konfiguracja

## Planowane funkcje (roadmap)

### [1.1.0] - Planowana
- [ ] Wsparcie dla JUnit 5 testing framework
- [ ] Automatyczne uruchamianie testów podczas kompilacji
- [ ] Wsparcie dla Spring Boot
- [ ] Template projektu dla różnych typów aplikacji
- [ ] Integracja z IDE (VS Code, IntelliJ)

### [1.2.0] - Planowana
- [ ] Wsparcie dla Gradle jako alternatywa dla Maven
- [ ] Hot reload podczas developmentu
- [ ] Profiling i monitoring wydajności
- [ ] Docker integration
- [ ] CI/CD template

### [2.0.0] - Planowana
- [ ] Wsparcie dla JDK 21 LTS
- [ ] Native compilation z GraalVM
- [ ] Microservices template
- [ ] Cloud deployment integration

## Wymagania systemowe

### Minimalne
- PlatformIO Core 6.0+
- Python 3.7+
- 500MB wolnego miejsca na dysku
- Połączenie internetowe (pierwsza instalacja)

### Zalecane
- PlatformIO Core 6.1+
- Python 3.9+
- 1GB wolnego miejsca na dysku
- SSD dla lepszej wydajności

## Znanego problemy

### [1.0.0]
- Windows: Długie ścieżki mogą powodować problemy z ekstraktowaniem JDK
- macOS: Może wymagać dodatkowych uprawnień dla pobranych plików
- Linux: Niektóre dystrybucje mogą wymagać instalacji dodatkowych pakietów

## Podziękowania

- Oracle Corporation za udostępnienie JDK
- Apache Software Foundation za Maven
- PlatformIO za framework platformy
- Społeczność Java za niesamowite biblioteki open source

## Licencja

MIT License - Zobacz [LICENSE](LICENSE) dla szczegółów.
