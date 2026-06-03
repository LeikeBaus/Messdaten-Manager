# Messdaten-Manager

## Projektbeschreibung:
Zielsetzung:
Ziel des Projektes ist die Entwicklung einer modularen GUI-Anwendung unter Verwendung von PyQt, die typische Aufgaben im Umgang mit technischen Messdaten abbildet.

## Funktionsumfang:
- Auswahl von physikalischen Größen
- Versuch mit Messdaten erfassen
- Speichern von Messdaten in Dateien
- Import von Messdaten (z.b. csv oder json)
- Übersicht/Auswahl von Versuchen (File-Manager)
- Plotten von 2D-Daten mit PyQt-Graph
- Speichern von Plots (optional)

## Systemarchitektur
MVC-Architektur
### Model
- Verwalten von Messdaten
- Import und Export von Dateien
- Dateisystemzugriff

### View
- PyQt Benutzeroberfläche
- Anzeige von Versuchen
- Anzeige von Graphen

### Controller
- Verbindung zwischen GUI und Datenmodell
- Verarbeitung von Benutzeraktionen

## User stories:
- Als Benutzer möchte ich Versuche direkt erfassen können.
- Als Benutzer möchte ich neben den Messdaten auch Metadaten erfassen können.
- Als Benutzer möchte ich Dateien importieren können.
- Als Benutzer möchte ich Messdateien graphisch vergleichen.
- Als Benutzer möchte ich zwischen physikalischen Größen auswählen können.
- Als Benutzer möchte ich Versuche in einer Liste sehen, um sie schnell auswählen zu können.
- Als Benutzer möchte ich Dateien exportieren können.

## Anforderungen
### Funktionale Anforderungen
- Das System muss ein einheitliches Datenformat verarbeiten können.
- Das System muss Messdaten aus CSV und JSON Dateien importieren können.
- Das System muss es ermöglichen, Metadaten erfassen zu können.
- Das System muss es ermöglichen, neue Experimente erfassen zu können.
- Das System muss Messdaten als 2D-Graph visualisieren können.
- Das System muss ermöglichen, die Achsen von dem Plot beschriften zu können.
- Das System muss ermöglichen, eine physikalische Größe einer Achse zuweiusen zu können.
- Das System muss eine Legende enthalten.
- Das System muss Messdaten in einem einheitlichen Format abspeichern können.
- Das System soll sämtliche Dateien im Projektordner verwalten können.
- Das System soll Plots speichern können.
- Das System soll es ermöglichen, das Styling von Plots zu ändern.

### Nicht-funktionale Anforderungen
- Die Anwendung muss fehlerhafte Importdateien erkennen und robust behandeln können.
- Die Anwendung soll größere Messdaten performant darstellen können.
- Die Anwendung soll eine intuitive Benutzeroberfläche bieten.
- Die Anwendung soll gut mit schlecht skalierten Daten umgehen können.
- Die Anwendung soll modular aufgebaut sein.
- Die Anwendung soll Betriebtssytem-übergreifend ausführbar sein.

## Ordnerstruktur
messdaten-manager/
│
├── model/
│   ├── experiment.py # Experiment-Klasse
│   ├── measurement_data.py # Messdaten-Klasse
│   └── experiment_repository.py # Verwaltet Experimente, suchen, laden, speichern, etc.
│
├── view/
│   ├── main_window.py
│   ├── experiment_list_view.py
│   ├── plot_view.py
│   └── dialogs/
│       ├── import_dialog.py
│       └── export_dialog.py
│
├── controller/
│   ├── experiment_controller.py
│   ├── import_controller.py
│   ├── export_controller.py
│   └── plot_controller.py
│
├── services/
│   ├── importers/
│   │   ├── importer.py # Abstraktes Interface für csv, json,... importer
│   │   ├── csv_importer.py
│   │   └── json_importer.py
│   │
│   └── exporters/
│       ├── exporter.py # Abstraktes Interface für csv, json,... exporter
│       ├── csv_exporter.py
│       └── json_exporter.py
│       └── plot_exporter.py
│
├── data/
│   └── experiments/ # Speicherort für Versuche
│
├── config.json # Alle settings
├── main.py # Einstiegspunkt. Initialisiert GUI und Controller. Soll möglichst wenig Geschäftslogik enthalten.
└── README.md
