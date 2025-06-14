# Java Platform for PlatformIO

Przykład podstawowego projektu Java używającego platformy PlatformIO z automatycznym pobieraniem JDK 18 i zarządzaniem zależnościami Maven.

## Funkcje

- **Automatyczne pobieranie JDK 18**: Platforma automatycznie pobiera i instaluje JDK 18
- **Zarządzanie zależnościami Maven**: Zależności z `lib_deps` są automatycznie konwertowane do formatu Maven
- **Integracja z PlatformIO**: Pełna integracja z workflow PlatformIO

## Użyte biblioteki

Ten przykład demonstruje użycie popularnych bibliotek Java:

- **Apache Commons Lang 3**: Narzędzia do pracy z String i podstawowymi typami
- **Apache Commons Collections 4**: Zaawansowane kolekcje i narzędzia
- **SLF4J**: Logging framework

## Kompilacja i uruchomienie

```bash
# Kompilacja
pio run

# Packaging (tworzenie JAR)
pio run -t upload

# Uruchomienie (jeśli skonfigurowane)
java -jar .pio/build/generic/target/*.jar
```

## Struktura projektu

```
basic-java/
├── src/
│   └── main/
│       └── java/
│           └── Main.java          # Główna klasa aplikacji
├── platformio.ini                 # Konfiguracja PlatformIO
└── README.md                      # Ten plik
```

## Konfiguracja zależności

Zależności definiuje się w sekcji `lib_deps` w pliku `platformio.ini`:

```ini
lib_deps = 
    org.apache.commons:commons-lang3@3.12.0
    org.apache.commons:commons-collections4@4.4
    org.slf4j:slf4j-api@2.0.7
    org.slf4j:slf4j-simple@2.0.7
```

Platforma automatycznie:
1. Konwertuje te zależności do formatu Maven (pom.xml)
2. Pobiera i instaluje JDK 18
3. Pobiera i instaluje Maven
4. Instaluje wszystkie zależności
5. Kompiluje projekt
