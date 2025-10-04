# Contributing to GDPR Deletion Tool

Vielen Dank für Ihr Interesse, zu diesem Projekt beizutragen! 🎉

## Wie kann ich beitragen?

### Fehler melden

Wenn Sie einen Fehler gefunden haben:

1. Prüfen Sie, ob der Fehler bereits gemeldet wurde
2. Öffnen Sie ein neues Issue mit:
   - Beschreibung des Problems
   - Schritte zur Reproduktion
   - Erwartetes vs. tatsächliches Verhalten
   - System-Informationen (OS, Python-Version)
   - Relevante Logs

### Features vorschlagen

Für neue Features:

1. Öffnen Sie ein Issue mit dem Tag "enhancement"
2. Beschreiben Sie:
   - Das Problem, das gelöst werden soll
   - Ihre vorgeschlagene Lösung
   - Alternativen, die Sie erwogen haben

### Code beitragen

1. **Fork** das Repository
2. **Clone** Ihren Fork
3. **Branch** erstellen: `git checkout -b feature/amazing-feature`
4. **Änderungen** vornehmen
5. **Tests** hinzufügen/aktualisieren
6. **Commit**: `git commit -m 'Add amazing feature'`
7. **Push**: `git push origin feature/amazing-feature`
8. **Pull Request** öffnen

## Entwicklungsrichtlinien

### Code-Stil

- **PEP 8** für Python-Code
- **Type Hints** verwenden
- **Docstrings** für Funktionen und Klassen
- **Kommentare** für komplexe Logik

### Tests

- Neue Features benötigen Tests
- Bestehende Tests dürfen nicht brechen
- Mindestens 80% Code Coverage

```bash
# Tests ausführen
pytest

# Mit Coverage
pytest --cov=src --cov-report=html
```

### Commits

Verwenden Sie aussagekräftige Commit-Nachrichten:

```
feat: Add response analysis with AI
fix: Correct SMTP connection timeout
docs: Update setup instructions
test: Add tests for email sender
refactor: Simplify database queries
```

Präfixe:
- `feat`: Neues Feature
- `fix`: Bugfix
- `docs`: Dokumentation
- `test`: Tests
- `refactor`: Code-Refactoring
- `style`: Formatierung
- `chore`: Wartung

### Pull Requests

- Beschreiben Sie Ihre Änderungen
- Referenzieren Sie relevante Issues
- Stellen Sie sicher, dass CI-Tests bestehen
- Aktualisieren Sie die Dokumentation

## Projektstruktur

```
src/
├── core/          # Kernfunktionalität
├── ai/            # KI-Integration
├── communication/ # E-Mail, Web-Automatisierung
├── workflow/      # Workflow-Orchestrierung
└── utils/         # Hilfsfunktionen

tests/             # Tests
docs/              # Dokumentation
```

## Entwicklungsumgebung

```bash
# Repository klonen
git clone https://github.com/yourusername/gdpr-deletion-tool.git
cd gdpr-deletion-tool

# Virtuelle Umgebung
python -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Fragen?

- Öffnen Sie ein Issue
- Starten Sie eine Discussion
- Kontaktieren Sie die Maintainer

## Code of Conduct

Seien Sie respektvoll und konstruktiv. Wir wollen eine einladende Community für alle.

## Lizenz

Durch Beiträge stimmen Sie zu, dass Ihre Beiträge unter der MIT-Lizenz lizenziert werden.
