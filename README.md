# Messdaten-Manager

## Projektbeschreibung:
Zielsetzung:
Ziel des Projektes ist die Entwicklung einer modularen GUI-Anwendung unter Verwendung von PyQt, die typische Aufgaben im Umgang mit technischen Messdaten abbildet.

## Funktionsumfang:
- Anlegen, Laden, Speichern und Loeschen von Experimenten
- Import von Experimenten oder Messreihen aus CSV und JSON
- Verwaltung von Messreihen innerhalb eines Experiments (anlegen, loeschen, speichern)
- Anzeige von Metadaten (Titel, Autor, Datum, Beschreibung, Kommentar)
- Tabellenansicht der Messdaten zur aktuell ausgewaehlten Messreihe
- Plotten von 2D-Daten mit pyqtgraph
- Beim Auswaehlen eines Experiments werden alle vorhandenen Messreihen geplottet
- Beim Auswaehlen einer Messreihe wird nur diese Messreihe dargestellt
- Plot-Export ist als Menuepunkt vorhanden, aber aktuell nicht in den Workflow integriert

## Systemarchitektur
MVC-Architektur
### Model
- Datenklassen fuer Experiment, Messreihe und Messdaten
- Repository fuer In-Memory-Verwaltung von Experimenten
- Konvertierung von Rohwerten in numerische XY-Reihen fuer den Plot

### View
- PyQt6-Oberflaeche mit Main Window, Menue, Toolbar und Seitenleiste
- Baumansicht fuer Experimente und Messreihen
- Tabellenansicht fuer Messdaten und Meta-Ansicht fuer Experimentinformationen
- Plot-Ansicht mit Legende, Achsenbeschriftung und mehreren Datenreihen
- Qt-Modelle fuer Baum- und Tabellenbindung

### Controller
- Orchestrierung der Benutzeraktionen ueber den zentralen ExperimentController
- Auswahlkontext, View-Update und Persistenz als getrennte Controller-Komponenten
- Import/Persistenz ueber austauschbare Importer (CSV/JSON)
- Laden von Workspace-Experimenten aus data/experiments beim Start

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
- messdaten-manager/
- │
- ├── controller/
- │   ├── experiment_controller.py
- │   ├── experiment_persistence.py
- │   ├── experiment_view_updater.py
- │   └── selection_context.py
- │
- ├── model/
- │   ├── experiment.py
- │   ├── experiment_repository.py
- │   └── measurement_data.py
- │
- ├── view/
- │   ├── app_actions.py
- │   ├── data_view.py
- │   ├── experiment_list_view.py
- │   ├── import_dialog.py
- │   ├── main_window.py
- │   ├── meta_view.py
- │   ├── plot_view.py
- │   ├── partials/
- │   │   ├── menubar.py
- │   │   └── toolbar.py
- │   └── qt_models/
- │       ├── experiment_tree_model.py
- │       └── measurement_table_model.py
- │
- ├── services/
- │   ├── exporters/
- │   │   ├── exporter.py
- │   │   ├── csv_exporter.py
- │   │   ├── json_exporter.py
- │   │   └── plot_exporter.py
- │   └── importers/
- │       ├── importer.py
- │       ├── csv_importer.py
- │       └── json_importer.py
- │
- ├── data/
- │   └── experiments/ (Speicherort fuer Versuche)
- │
- ├── exports/
- │
- ├── config.json
- ├── main.py
- ├── requirements.txt
- └── README.md
