# Setup Guide

Detaillierte Anleitung zur Installation und Konfiguration des GDPR Deletion Tools.

## Voraussetzungen

### System-Anforderungen

- **Betriebssystem**: Linux, macOS, oder Windows
- **Python**: Version 3.10 oder höher
- **RAM**: Mindestens 4 GB (8 GB empfohlen für AI-Features)
- **Speicherplatz**: ~2 GB für Ollama-Modelle

### Erforderliche Software

1. **Python 3.10+**
   ```bash
   # Überprüfen der Python-Version
   python --version
   # oder
   python3 --version
   ```

2. **Git**
   ```bash
   git --version
   ```

3. **Ollama** (optional, für AI-Features)
   - Download: https://ollama.ai
   - Installation:
     ```bash
     # Linux
     curl -fsSL https://ollama.ai/install.sh | sh
     
     # macOS
     brew install ollama
     
     # Windows
     # Download installer from https://ollama.ai
     ```

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/yourusername/gdpr-deletion-tool.git
cd gdpr-deletion-tool
```

### 2. Virtuelle Umgebung erstellen

```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Ollama einrichten (optional)

```bash
# Ollama starten
ollama serve

# In einem neuen Terminal: Modell herunterladen
ollama pull llama2

# Alternativ: kleineres Modell
ollama pull mistral

# Verfügbare Modelle anzeigen
ollama list
```

## Konfiguration

### 1. Umgebungsvariablen

```bash
# .env-Datei erstellen
cp .env.example .env

# .env bearbeiten
nano .env  # oder vim, code, etc.
```

### 2. SMTP konfigurieren

#### Gmail (empfohlen für Tests)

1. **App-Passwort erstellen**:
   - Google-Konto → Sicherheit → 2-Faktor-Authentifizierung
   - App-Passwörter → "Mail" auswählen
   - Passwort kopieren

2. **.env konfigurieren**:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=ihre-email@gmail.com
   SMTP_PASSWORD=ihr-app-passwort
   SENDER_EMAIL=ihre-email@gmail.com
   SENDER_NAME=Ihr Name
   ```

#### Andere SMTP-Anbieter

**Outlook/Hotmail**:
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo**:
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Eigener Server**:
```env
SMTP_SERVER=mail.ihredomain.de
SMTP_PORT=587
SMTP_USERNAME=user@ihredomain.de
SMTP_PASSWORD=passwort
```

### 3. Ollama konfigurieren

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

### 4. Weitere Einstellungen

```env
# Sprache
DEFAULT_LANGUAGE=de  # oder 'en'

# Automatisierung
AUTO_SEND_ENABLED=false
RETRY_DELAY_DAYS=14
ESCALATION_DELAY_DAYS=30

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## Initialisierung

```bash
# Tool initialisieren
python main.py init
```

Dies erstellt:
- Datenbank-Schema
- Notwendige Verzeichnisse
- Testet Verbindungen

## Verbindungen testen

### SMTP testen

```bash
python main.py test-smtp
```

Erwartete Ausgabe:
```
✓ SMTP connection successful
```

### Ollama testen

```bash
python main.py test-ollama
```

Erwartete Ausgabe:
```
✓ Ollama is running
Available models: llama2, mistral
```

## Erste Schritte

### 1. Unternehmen hinzufügen

```bash
python main.py add-company \
  --name "Google LLC" \
  --email "privacy-eu@google.com" \
  --website "https://www.google.com"
```

### 2. Löschanfrage erstellen

```bash
python main.py create-request \
  --company "Google LLC" \
  --user-name "Max Mustermann" \
  --user-email "max@example.com" \
  --reason "Ich nutze den Dienst nicht mehr"
```

### 3. Status überprüfen

```bash
python main.py status
```

### 4. Anfrage senden

```bash
python main.py send-request --id 1
```

## Fehlerbehebung

### Problem: "SMTP connection failed"

**Lösung**:
1. Überprüfen Sie SMTP-Zugangsdaten in `.env`
2. Bei Gmail: App-Passwort verwenden (nicht normales Passwort)
3. Firewall-Einstellungen prüfen
4. Port 587 oder 465 versuchen

### Problem: "Ollama is not running"

**Lösung**:
1. Ollama starten: `ollama serve`
2. Überprüfen: `curl http://localhost:11434/api/tags`
3. Modell herunterladen: `ollama pull llama2`

### Problem: "ModuleNotFoundError"

**Lösung**:
```bash
# Virtuelle Umgebung aktiviert?
source venv/bin/activate

# Abhängigkeiten neu installieren
pip install -r requirements.txt
```

### Problem: "Permission denied" bei Logs

**Lösung**:
```bash
# Verzeichnis-Berechtigungen setzen
chmod 755 logs/
chmod 755 data/
```

## Erweiterte Konfiguration

### Automatische Ausführung (Cron)

```bash
# Crontab bearbeiten
crontab -e

# Täglich um 9:00 Uhr ausstehende Tasks ausführen
0 9 * * * cd /pfad/zum/projekt && /pfad/zum/projekt/venv/bin/python main.py auto-followup
```

### Systemd Service (Linux)

```bash
# Service-Datei erstellen
sudo nano /etc/systemd/system/gdpr-tool.service
```

```ini
[Unit]
Description=GDPR Deletion Tool Auto-Followup
After=network.target

[Service]
Type=oneshot
User=youruser
WorkingDirectory=/pfad/zum/projekt
ExecStart=/pfad/zum/projekt/venv/bin/python main.py auto-followup

[Install]
WantedBy=multi-user.target
```

```bash
# Timer erstellen
sudo nano /etc/systemd/system/gdpr-tool.timer
```

```ini
[Unit]
Description=Run GDPR Tool daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# Aktivieren
sudo systemctl enable gdpr-tool.timer
sudo systemctl start gdpr-tool.timer
```

## Sicherheitshinweise

1. **Niemals** `.env` in Git committen
2. Regelmäßig Backups der Datenbank erstellen
3. SMTP-Passwörter sicher aufbewahren
4. Logs regelmäßig rotieren
5. Verschlüsselung für sensible Daten aktivieren

## Nächste Schritte

- [Nutzungsanleitung](USAGE.md)
- [Rechtliche Hinweise](LEGAL.md)
- [API-Dokumentation](API.md)
