# 🔒 Automatisierte DSGVO-Löschanfragen mit Open-Source-KI
[☕ Unterstützen: Buy me a coffee](https://buymeacoffee.com/louziusmedia)
[![CI](https://github.com/LouziusMedia/LoeschMich/actions/workflows/ci.yml/badge.svg)](https://github.com/LouziusMedia/LoeschMich/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Ein kostenfreies, Open-Source-Tool zur automatisierten Erstellung und Verwaltung von DSGVO-Löschanfragen (Art. 17 DSGVO) mit lokaler KI-Unterstützung.

## 🎯 Projektziel

Dieses Tool ermöglicht es Nutzern, ihre Rechte nach der DSGVO effizient wahrzunehmen, indem es:
- Personalisierte Löschanfragen automatisch generiert
- E-Mails an Unternehmen versendet
- Antworten verfolgt und analysiert
- Erinnerungen und Eskalationen verwaltet
- **Vollständig lokal und datenschutzfreundlich arbeitet**

## ✨ Features

- 🤖 **Lokale KI-Integration** mit Ollama (keine Cloud-Dienste erforderlich)
- 📧 **Automatischer E-Mail-Versand** mit SMTP
- 📊 **Status-Tracking** und Fortschrittsverfolgung
- 🔄 **Automatische Nachverfolgung** bei fehlenden Antworten
- 🌐 **Web-Formular-Automatisierung** (optional mit Selenium)
- 🔐 **Datenschutzkonform** - alle Daten bleiben lokal
- 📝 **DSGVO-konforme Vorlagen** basierend auf datenanfragen.de
- 🇩🇪 **Mehrsprachig** (Deutsch, Englisch)

## 🚀 Quick Start

### Voraussetzungen

- Python 3.10 oder höher
- Ollama installiert ([Installation](https://ollama.ai))
- SMTP-Zugang (z.B. Gmail mit App-Passwort)

### Installation

```bash
# Repository klonen
git clone https://github.com/LouziusMedia/LoeschMich.git
cd LoeschMich

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Ollama-Modell herunterladen
ollama pull llama2

# Umgebungsvariablen konfigurieren
cp .env.example .env
# Bearbeite .env mit deinen Daten
```

### Erste Schritte

```bash
# Unternehmen zur Datenbank hinzufügen
python main.py add-company --name "Beispiel GmbH" --email "datenschutz@beispiel.de"

# Löschanfrage erstellen
python main.py create-request --company "Beispiel GmbH" --reason "Ich möchte meine Daten löschen lassen"

# Anfrage senden
python main.py send-request --id 1

# Status überprüfen
python main.py status
```

## 📁 Projektstruktur

```
gdpr-deletion-tool/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py          # SQLite-Datenbankverwaltung
│   │   ├── models.py             # Datenmodelle (Pydantic)
│   │   └── config.py             # Konfigurationsverwaltung
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── ollama_client.py      # Ollama-Integration
│   │   ├── request_generator.py  # KI-gestützte Anfragenerstellung
│   │   └── response_analyzer.py  # Antwortanalyse
│   ├── communication/
│   │   ├── __init__.py
│   │   ├── email_sender.py       # E-Mail-Versand
│   │   └── web_automation.py     # Selenium-Automatisierung
│   ├── workflow/
│   │   ├── __init__.py
│   │   ├── orchestrator.py       # Workflow-Steuerung
│   │   └── scheduler.py          # Zeitplanung
│   └── utils/
│       ├── __init__.py
│       ├── logger.py             # Logging-Konfiguration
│       ├── encryption.py         # Datenverschlüsselung
│       └── templates.py          # DSGVO-Vorlagen
├── templates/
│   ├── deletion_request_de.txt
│   ├── deletion_request_en.txt
│   └── reminder_de.txt
├── data/
│   ├── companies.json            # Beispiel-Unternehmensdaten
│   └── .gitkeep
├── tests/
│   ├── test_ai.py
│   ├── test_email.py
│   └── test_database.py
├── docs/
│   ├── SETUP.md
│   ├── USAGE.md
│   └── LEGAL.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── main.py                       # Haupteinstiegspunkt
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## 🔧 Konfiguration

Bearbeite die `.env`-Datei mit deinen Einstellungen:

```env
# SMTP für E-Mail-Versand
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=deine-email@gmail.com
SMTP_PASSWORD=dein-app-passwort

# Ollama (lokal)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

## 📚 Verwendung

### CLI-Befehle

```bash
# Unternehmen verwalten
python main.py add-company --name "Firma" --email "email@firma.de"
python main.py list-companies

# Anfragen erstellen und senden
python main.py create-request --company "Firma" --type deletion
python main.py send-request --id 1
python main.py send-all-pending

# Status und Tracking
python main.py status
python main.py check-responses

# Automatisierung
python main.py auto-followup  # Automatische Nachverfolgung
```

### Als Python-Modul

```python
from src.core.database import Database
from src.ai.request_generator import RequestGenerator
from src.communication.email_sender import EmailSender

# Datenbank initialisieren
db = Database()

# Anfrage mit KI generieren
generator = RequestGenerator()
request_text = generator.generate_deletion_request(
    company_name="Beispiel GmbH",
    user_data={"name": "Max Mustermann", "email": "max@example.com"}
)

# E-Mail senden
sender = EmailSender()
sender.send_request(
    to_email="datenschutz@beispiel.de",
    subject="DSGVO Löschantrag gemäß Art. 17 DSGVO",
    body=request_text
)
```

## 🤖 KI-Integration

Das Tool nutzt **Ollama** für lokale, datenschutzfreundliche KI:

- **Textgenerierung**: Personalisierte DSGVO-Anfragen
- **Antwortanalyse**: Automatische Auswertung von Unternehmensantworten
- **Priorisierung**: Intelligente Nachverfolgung

Unterstützte Modelle:
- `llama2` (empfohlen)
- `mistral`
- `codellama`

## 🔐 Datenschutz & Sicherheit

- ✅ Alle Daten werden **lokal** gespeichert
- ✅ Keine Cloud-Dienste erforderlich
- ✅ Sensible Daten werden verschlüsselt
- ✅ SMTP-Zugangsdaten in `.env` (nicht im Repo)
- ✅ Open-Source und transparent

> Hinweis: Im CI läuft ein wöchentlicher, nicht-blockierender Security-Check (safety/bandit). Ergebnisse werden in Pull Requests als Kommentar zusammengefasst.

## 📖 Rechtliche Grundlagen

Dieses Tool basiert auf:
- **Art. 17 DSGVO** - Recht auf Löschung ("Recht auf Vergessenwerden")
- **Art. 15 DSGVO** - Auskunftsrecht
- Vorlagen von [datenanfragen.de](https://www.datenanfragen.de)

⚠️ **Haftungsausschluss**: Dieses Tool dient der Automatisierung. Die rechtliche Verantwortung liegt beim Nutzer.

## 🧪 Tests

```bash
# Alle Tests ausführen
pytest

# Mit Coverage
pytest --cov=src --cov-report=html

# Spezifische Tests
pytest tests/test_ai.py
```

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:
1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der **MIT-Lizenz** lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- [datenanfragen.de](https://www.datenanfragen.de) für DSGVO-Vorlagen
- [Ollama](https://ollama.ai) für lokale KI-Modelle
- Die Open-Source-Community



## 🗺️ Roadmap

- [x] Grundlegende DSGVO-Anfragenerstellung
- [x] E-Mail-Versand
- [x] Lokale KI-Integration
- [ ] Web-Formular-Automatisierung
- [ ] GUI (Webinterface)
- [ ] Mehrsprachigkeit erweitern
- [ ] Integration mit n8n
- [ ] Mobile App

---

**Hinweis**: Dieses Tool befindet sich in aktiver Entwicklung. Feedback und Beiträge sind herzlich willkommen!
