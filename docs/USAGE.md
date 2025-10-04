# Nutzungsanleitung

Detaillierte Anleitung zur Verwendung des GDPR Deletion Tools.

## Übersicht

Das Tool bietet folgende Hauptfunktionen:
- Verwaltung von Unternehmen
- Erstellung von DSGVO-Löschanfragen
- Automatischer E-Mail-Versand
- Status-Tracking
- Automatische Nachverfolgung

## CLI-Befehle

### Initialisierung

```bash
python main.py init
```

Initialisiert das Tool und testet alle Verbindungen.

### Unternehmensverwaltung

#### Unternehmen hinzufügen

```bash
python main.py add-company \
  --name "Firmenname" \
  --email "datenschutz@firma.de" \
  --website "https://firma.de" \
  --address "Straße 1, 12345 Stadt" \
  --notes "Optionale Notizen"
```

**Pflichtfelder**:
- `--name`: Firmenname
- `--email`: E-Mail-Adresse für Datenschutzanfragen

**Optional**:
- `--website`: Unternehmenswebsite
- `--dpo`: Datenschutzbeauftragter
- `--address`: Postanschrift
- `--notes`: Zusätzliche Notizen

#### Unternehmen auflisten

```bash
python main.py list-companies
```

Zeigt alle gespeicherten Unternehmen mit ID, Name und E-Mail.

### Anfragen erstellen

#### Neue Löschanfrage

```bash
python main.py create-request \
  --company "Firmenname" \
  --user-name "Max Mustermann" \
  --user-email "max@example.com" \
  --reason "Ich nutze den Dienst nicht mehr" \
  --language de
```

**Parameter**:
- `--company`: Firmenname (oder `--company-id` für ID)
- `--user-name`: Ihr Name (optional)
- `--user-email`: Ihre E-Mail (optional)
- `--reason`: Begründung für die Löschung (optional, aber empfohlen)
- `--language`: Sprache (`de` oder `en`, Standard: `de`)
- `--send`: Sofort senden (optional)

**Beispiele**:

```bash
# Einfache Anfrage
python main.py create-request --company "Google LLC"

# Mit Begründung und sofortigem Versand
python main.py create-request \
  --company "Facebook" \
  --reason "Datenschutzbedenken" \
  --send

# Mit vollständigen Angaben
python main.py create-request \
  --company "Amazon" \
  --user-name "Max Mustermann" \
  --user-email "max@example.com" \
  --reason "Account wird nicht mehr genutzt" \
  --language de
```

### Anfragen versenden

#### Einzelne Anfrage senden

```bash
python main.py send-request --id 1
```

#### Alle ausstehenden Anfragen senden

```bash
python main.py send-request --all
```

### Status überprüfen

#### Alle Anfragen anzeigen

```bash
python main.py status
```

Zeigt Übersicht aller Anfragen mit:
- ID
- Unternehmen
- Typ
- Status
- Erstellungsdatum

#### Details einer Anfrage

```bash
python main.py status --id 1
```

Zeigt detaillierte Informationen:
- Vollständige Anfrage
- Zeitstempel
- Anzahl Erinnerungen
- Notizen

### Antworten verarbeiten

#### Antwort aus Datei

```bash
python main.py process-response --id 1 --file antwort.txt
```

#### Antwort interaktiv eingeben

```bash
python main.py process-response --id 1
# Dann Text eingeben und mit Ctrl+D beenden
```

Das Tool analysiert die Antwort automatisch und:
- Erkennt den Typ (bestätigt, abgeschlossen, abgelehnt, etc.)
- Erstellt eine Zusammenfassung
- Schlägt nächste Schritte vor
- Aktualisiert den Status

### Automatische Nachverfolgung

```bash
python main.py auto-followup
```

Führt alle ausstehenden automatischen Aufgaben aus:
- Sendet Erinnerungen nach 14 Tagen
- Sendet Eskalationen nach 30 Tagen
- Aktualisiert Status

**Empfehlung**: Als Cronjob einrichten (siehe SETUP.md)

### Verbindungstests

#### SMTP testen

```bash
python main.py test-smtp
```

#### Ollama testen

```bash
python main.py test-ollama
```

## Workflows

### Workflow 1: Einfache Löschanfrage

```bash
# 1. Unternehmen hinzufügen (einmalig)
python main.py add-company \
  --name "Beispiel GmbH" \
  --email "datenschutz@beispiel.de"

# 2. Anfrage erstellen und senden
python main.py create-request \
  --company "Beispiel GmbH" \
  --reason "Ich möchte meine Daten löschen lassen" \
  --send

# 3. Status überprüfen
python main.py status
```

### Workflow 2: Mehrere Unternehmen

```bash
# 1. Unternehmen importieren (aus companies.json)
python main.py add-company --name "Google" --email "privacy-eu@google.com"
python main.py add-company --name "Facebook" --email "mydataprivacyrights@support.facebook.com"
python main.py add-company --name "Amazon" --email "eu-privacy@amazon.de"

# 2. Anfragen für alle erstellen
python main.py create-request --company "Google" --reason "Nicht mehr genutzt"
python main.py create-request --company "Facebook" --reason "Nicht mehr genutzt"
python main.py create-request --company "Amazon" --reason "Nicht mehr genutzt"

# 3. Alle auf einmal senden
python main.py send-request --all

# 4. Status überprüfen
python main.py status
```

### Workflow 3: Mit Nachverfolgung

```bash
# 1. Anfrage erstellen und senden
python main.py create-request --company "Firma" --send

# 2. Nach 2 Wochen: Automatische Erinnerung
python main.py auto-followup

# 3. Antwort verarbeiten
echo "Ihre Daten wurden gelöscht" | python main.py process-response --id 1

# 4. Status prüfen
python main.py status --id 1
```

## Python-API

### Als Modul verwenden

```python
from src.core.database import Database
from src.core.models import Company, RequestType
from src.workflow.orchestrator import WorkflowOrchestrator

# Datenbank initialisieren
db = Database()

# Unternehmen hinzufügen
company = Company(
    name="Beispiel GmbH",
    email="datenschutz@beispiel.de"
)
company_id = db.add_company(company)
company.id = company_id

# Orchestrator erstellen
orchestrator = WorkflowOrchestrator(db)

# Anfrage erstellen und senden
request_id = orchestrator.create_and_send_request(
    company=company,
    user_name="Max Mustermann",
    user_email="max@example.com",
    reason="Ich nutze den Dienst nicht mehr",
    language="de",
    auto_send=True
)

print(f"Anfrage {request_id} wurde gesendet")
```

### Nur Textgenerierung

```python
from src.ai.request_generator import RequestGenerator
from src.core.models import Company

generator = RequestGenerator(use_ai=True)

company = Company(
    id=1,
    name="Beispiel GmbH",
    email="datenschutz@beispiel.de"
)

subject, body = generator.generate_deletion_request(
    company=company,
    user_name="Max Mustermann",
    reason="Datenschutzgründe"
)

print(f"Betreff: {subject}")
print(f"\n{body}")
```

### Antworten analysieren

```python
from src.ai.response_analyzer import ResponseAnalyzer

analyzer = ResponseAnalyzer(use_ai=True)

response_text = """
Sehr geehrter Herr Mustermann,
wir haben Ihre Anfrage erhalten und werden diese innerhalb 
der gesetzlichen Frist bearbeiten.
"""

analysis = analyzer.analyze_response(response_text)

print(f"Typ: {analysis['type']}")
print(f"Zusammenfassung: {analysis['summary']}")
print(f"Aktion erforderlich: {analysis['action_required']}")
print(f"Empfehlung: {analysis['suggested_action']}")
```

## Tipps & Best Practices

### 1. Begründung angeben

Auch wenn nicht verpflichtend, erhöht eine Begründung die Erfolgswahrscheinlichkeit:

```bash
--reason "Ich nutze den Dienst seit über einem Jahr nicht mehr"
--reason "Ich habe Datenschutzbedenken"
--reason "Ich möchte meine Online-Präsenz reduzieren"
```

### 2. Identifikationsdaten bereitstellen

Für schnellere Bearbeitung:

```bash
--user-name "Ihr vollständiger Name"
--user-email "Die bei der Registrierung verwendete E-Mail"
```

### 3. Regelmäßig Status prüfen

```bash
# Wöchentlich
python main.py status

# Oder automatisch
python main.py auto-followup
```

### 4. Antworten dokumentieren

Speichern Sie Unternehmensantworten:

```bash
# E-Mail-Antwort in Datei speichern
cat > antwort.txt << EOF
[Antwort des Unternehmens]
EOF

# Verarbeiten
python main.py process-response --id 1 --file antwort.txt
```

### 5. Backups erstellen

```bash
# Datenbank sichern
cp data/gdpr_requests.db data/gdpr_requests.db.backup

# Oder mit Datum
cp data/gdpr_requests.db data/gdpr_requests.db.$(date +%Y%m%d)
```

## Häufige Szenarien

### Unternehmen antwortet nicht

```bash
# Nach 14 Tagen
python main.py auto-followup  # Sendet automatisch Erinnerung

# Nach 30 Tagen
python main.py auto-followup  # Sendet Eskalation
```

### Unternehmen lehnt ab

```bash
# Antwort verarbeiten
python main.py process-response --id 1 --file ablehnung.txt

# Status prüfen - zeigt Empfehlung
python main.py status --id 1
```

### Mehrere Accounts bei einem Unternehmen

```bash
# Separate Anfragen für jeden Account
python main.py create-request \
  --company "Google" \
  --user-email "account1@gmail.com" \
  --send

python main.py create-request \
  --company "Google" \
  --user-email "account2@gmail.com" \
  --send
```

## Fehlerbehebung

### "Company not found"

```bash
# Unternehmen zuerst hinzufügen
python main.py add-company --name "Firma" --email "email@firma.de"

# Oder vorhandene Unternehmen anzeigen
python main.py list-companies
```

### "Failed to send email"

```bash
# SMTP-Verbindung testen
python main.py test-smtp

# .env überprüfen
cat .env | grep SMTP
```

### Anfrage wurde nicht erstellt

```bash
# Logs überprüfen
tail -f logs/gdpr_tool.log

# Datenbank-Status prüfen
python main.py status
```

## Nächste Schritte

- [Setup-Anleitung](SETUP.md)
- [Rechtliche Hinweise](LEGAL.md)
- [Entwickler-Dokumentation](API.md)
