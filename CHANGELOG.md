# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Geplant
- Web-Interface (GUI)
- Integration mit n8n
- Mehrsprachigkeit erweitern (FR, IT, ES)
- Mobile App
- Automatische Formular-Ausfüllung mit Selenium
- Export-Funktionen (PDF, CSV)

## [0.1.0] - 2025-10-04

### Hinzugefügt
- Grundlegende CLI-Anwendung
- SQLite-Datenbankverwaltung
- DSGVO-Anfragengenerierung (Art. 17)
- E-Mail-Versand via SMTP
- Lokale KI-Integration mit Ollama
- Automatische Nachverfolgung (Erinnerungen, Eskalationen)
- Status-Tracking für Anfragen
- Response-Analyse mit KI
- DSGVO-konforme Vorlagen (DE/EN)
- Workflow-Orchestrierung
- Umfassende Dokumentation
- Unit-Tests
- CI/CD-Pipeline (GitHub Actions)
- Beispiel-Unternehmensdaten

### Features
- **Unternehmensverwaltung**: Hinzufügen, Auflisten, Aktualisieren
- **Anfragenerstellung**: Mit/ohne KI-Unterstützung
- **Automatischer Versand**: SMTP-Integration
- **Tracking**: Status, Fristen, Erinnerungen
- **AI-Features**: 
  - Textgenerierung mit Ollama
  - Antwortanalyse
  - Intelligente Priorisierung
- **Datenschutz**: Vollständig lokal, keine Cloud
- **Mehrsprachig**: Deutsch, Englisch

### Technisch
- Python 3.10+ Support
- Pydantic für Datenvalidierung
- SQLite für Datenspeicherung
- Jinja2 für Templates
- Pytest für Tests
- GitHub Actions für CI/CD

### Dokumentation
- README mit Quick Start
- Detaillierte Setup-Anleitung
- Umfassende Nutzungsanleitung
- Rechtliche Hinweise
- Contributing Guidelines
- MIT-Lizenz

## [0.0.1] - 2025-10-01

### Hinzugefügt
- Initiales Projekt-Setup
- Grundlegende Projektstruktur
- Erste Konzepte und Planung

---

## Versionshinweise

### Semantic Versioning

- **MAJOR** (1.0.0): Inkompatible API-Änderungen
- **MINOR** (0.1.0): Neue Features, abwärtskompatibel
- **PATCH** (0.0.1): Bugfixes, abwärtskompatibel

### Release-Zyklus

- **Unreleased**: Aktuelle Entwicklung
- **Beta**: Feature-komplett, Testing
- **Stable**: Produktionsreif

[Unreleased]: https://github.com/yourusername/gdpr-deletion-tool/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/gdpr-deletion-tool/releases/tag/v0.1.0
[0.0.1]: https://github.com/yourusername/gdpr-deletion-tool/releases/tag/v0.0.1
