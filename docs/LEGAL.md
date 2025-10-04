# Rechtliche Hinweise

## DSGVO-Grundlagen

### Artikel 17 DSGVO - Recht auf Löschung

Die betroffene Person hat das Recht, von dem Verantwortlichen zu verlangen, dass sie betreffende personenbezogene Daten unverzüglich gelöscht werden.

**Voraussetzungen**:
- Die Daten sind für die Zwecke nicht mehr notwendig
- Die betroffene Person widerruft ihre Einwilligung
- Die betroffene Person legt Widerspruch ein
- Die Daten wurden unrechtmäßig verarbeitet
- Die Löschung ist zur Erfüllung einer rechtlichen Verpflichtung erforderlich

**Ausnahmen** (Art. 17 Abs. 3 DSGVO):
- Ausübung des Rechts auf freie Meinungsäußerung
- Erfüllung einer rechtlichen Verpflichtung
- Gründe des öffentlichen Interesses
- Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen

### Artikel 15 DSGVO - Auskunftsrecht

Recht auf Auskunft über:
- Verarbeitungszwecke
- Kategorien personenbezogener Daten
- Empfänger der Daten
- Speicherdauer
- Bestehen weiterer Rechte

### Fristen

**Art. 12 Abs. 3 DSGVO**:
- Unverzügliche Beantwortung
- Spätestens innerhalb eines Monats
- Verlängerung um zwei Monate bei Komplexität möglich

## Verwendung dieses Tools

### Rechtliche Einordnung

Dieses Tool dient der **Automatisierung** von DSGVO-Anfragen. Es:
- Generiert rechtskonforme Anfragen
- Versendet diese per E-Mail
- Verfolgt den Status
- Erinnert bei fehlender Antwort

### Haftungsausschluss

⚠️ **WICHTIG**: 

1. **Keine Rechtsberatung**: Dieses Tool ersetzt keine Rechtsberatung
2. **Eigenverantwortung**: Die rechtliche Verantwortung liegt beim Nutzer
3. **Keine Garantie**: Erfolg der Anfragen kann nicht garantiert werden
4. **Prüfungspflicht**: Nutzer sollten generierte Texte vor Versand prüfen

### Empfohlene Vorgehensweise

1. **Prüfen Sie Ihre Berechtigung**
   - Haben Sie ein Konto beim Unternehmen?
   - Wurden Ihre Daten verarbeitet?
   - Liegt ein Löschungsgrund vor?

2. **Identifikation sicherstellen**
   - Verwenden Sie die bei Registrierung angegebenen Daten
   - Fügen Sie ggf. Kundennummer, Benutzername hinzu
   - Nutzen Sie die registrierte E-Mail-Adresse

3. **Begründung angeben**
   - Nicht verpflichtend, aber hilfreich
   - Erhöht Erfolgswahrscheinlichkeit
   - Vermeidet Rückfragen

4. **Antworten dokumentieren**
   - Speichern Sie alle Korrespondenz
   - Notieren Sie Fristen
   - Bewahren Sie Nachweise auf

## Umgang mit Ablehnungen

### Berechtigte Ablehnungen

Unternehmen dürfen ablehnen bei:
- Gesetzlichen Aufbewahrungspflichten (z.B. Steuerrecht)
- Laufenden Verträgen
- Berechtigten Interessen (z.B. Betrugsbekämpfung)
- Rechtlichen Ansprüchen

### Unberechtigte Ablehnungen

Wenn ein Unternehmen unberechtigt ablehnt:

1. **Nachfragen**
   - Begründung verlangen
   - Rechtsgrundlage erfragen

2. **Eskalieren**
   - Datenschutzbeauftragten kontaktieren
   - Geschäftsführung einbeziehen

3. **Beschwerde einreichen**
   - Bei zuständiger Datenschutzbehörde
   - Kostenlos und formlos möglich

### Datenschutzbehörden (Deutschland)

**Bundesbeauftragter**:
- Website: https://www.bfdi.bund.de
- E-Mail: poststelle@bfdi.bund.de

**Landesbehörden**: Je nach Bundesland
- Liste: https://www.bfdi.bund.de/DE/Infothek/Anschriften_Links/anschriften_links-node.html

**Österreich**:
- Website: https://www.dsb.gv.at

**Schweiz**:
- Website: https://www.edoeb.admin.ch

## Datenschutz des Tools

### Lokale Datenspeicherung

Dieses Tool speichert **alle Daten lokal**:
- SQLite-Datenbank auf Ihrem Computer
- Keine Cloud-Synchronisation
- Keine externen Server

### Verwendete Dienste

**Ollama (optional)**:
- Läuft lokal auf Ihrem Computer
- Keine Datenübertragung an Dritte
- Open-Source-Modelle

**SMTP**:
- Nutzt Ihren E-Mail-Provider
- Normale E-Mail-Kommunikation
- Verschlüsselt (TLS)

### Sicherheitsempfehlungen

1. **Verschlüsselung**
   - Festplattenverschlüsselung aktivieren
   - Sichere Passwörter verwenden

2. **Zugriffskontrolle**
   - Dateirechte einschränken
   - `.env` nicht weitergeben

3. **Backups**
   - Regelmäßig Datenbank sichern
   - Verschlüsselt aufbewahren

4. **Löschung**
   - Nach Abschluss Daten löschen
   - Datenbank sicher überschreiben

## Internationale Nutzung

### EU/EWR

DSGVO gilt für:
- Unternehmen in der EU
- Unternehmen, die EU-Bürger bedienen
- Verarbeitung in der EU

### Außerhalb EU

Andere Datenschutzgesetze:
- **UK**: UK GDPR (ähnlich DSGVO)
- **Schweiz**: DSG (Datenschutzgesetz)
- **USA**: CCPA (California), CPRA
- **Kanada**: PIPEDA
- **Brasilien**: LGPD

Dieses Tool kann angepasst werden, ist aber primär für DSGVO konzipiert.

## Musterbriefe und Vorlagen

### Quellen

Vorlagen basieren auf:
- https://www.datenanfragen.de
- Offizielle DSGVO-Texte
- Empfehlungen von Datenschutzbehörden

### Anpassung

Sie können Vorlagen anpassen:
- `src/utils/templates.py` bearbeiten
- Eigene Formulierungen verwenden
- Rechtlich geprüfte Texte einsetzen

### Sprachen

Aktuell unterstützt:
- Deutsch (de)
- Englisch (en)

Weitere Sprachen können hinzugefügt werden.

## Häufige rechtliche Fragen

### Muss ich eine Begründung angeben?

**Nein**, aber:
- Beschleunigt Bearbeitung
- Vermeidet Rückfragen
- Erhöht Erfolgswahrscheinlichkeit

### Kann ich für mehrere Personen Anfragen stellen?

**Nein**:
- Nur für eigene Daten
- Ausnahme: Gesetzliche Vertretung (z.B. Eltern für Kinder)
- Vollmacht erforderlich

### Was passiert bei Fristüberschreitung?

**Optionen**:
1. Erinnerung senden (automatisch nach 14 Tagen)
2. Eskalation (automatisch nach 30 Tagen)
3. Beschwerde bei Datenschutzbehörde
4. Rechtliche Schritte (Anwalt konsultieren)

### Muss das Unternehmen kostenlos löschen?

**Ja**:
- DSGVO-Anfragen sind grundsätzlich kostenlos
- Ausnahme: Offenkundig unbegründete/exzessive Anfragen

### Kann ich gelöschte Daten zurückfordern?

**Nein**:
- Löschung ist endgültig
- Sorgfältig überlegen vor Antragstellung
- Ggf. erst Auskunft (Art. 15) beantragen

## Weiterführende Ressourcen

### Offizielle Quellen

- **EU-DSGVO**: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Bundesdatenschutzgesetz**: https://www.gesetze-im-internet.de/bdsg_2018/
- **Datenanfragen.de**: https://www.datenanfragen.de

### Beratung

- Datenschutzbeauftragte
- Verbraucherzentralen
- Anwälte für Datenschutzrecht

### Community

- GitHub Discussions
- Datenschutz-Foren
- Verbraucherschutz-Organisationen

## Disclaimer

Dieses Dokument dient der Information und stellt keine Rechtsberatung dar. Bei rechtlichen Fragen konsultieren Sie bitte einen Fachanwalt für Datenschutzrecht.

**Stand**: Oktober 2025  
**Rechtsgrundlage**: DSGVO (EU) 2016/679
