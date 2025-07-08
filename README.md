# Phasely

## 🧪 Demo starten

Powershell:
pdm run streamlit run 00_Dashboard.py

## Autorinnen
- Sophia Gwiggner  
- Lilly Feifel

---

## 💡 Mission & Vision

Phasely ist eine datenbasierte Trainings-App, die auf den natürlichen Zyklus der Nutzerin eingeht. Ziel ist es, die Trainingsplanung an die hormonellen Veränderungen in den vier Zyklusphasen anzupassen und damit:

- körperliche Leistungsfähigkeit gezielt zu nutzen,
- Überlastung zu vermeiden,
- Wohlbefinden, Motivation und Regeneration zu fördern.

Die App hilft Nutzerinnen, Sporteinheiten auszuwählen und zeigt an, wie gut diese zur aktuellen Zyklusphase passen.

---

## 🛠️ Projekt installieren

1. Repository klonen  
   ```bash
   git clone <repo-url>
   cd phasely

2. Abhängigkeiten installieren (empfohlen mit PDM)
    ```bash
    pdm install

3. Auswahl der CSV-Datei
    in globals.py kann die gewünschte CSV-Datei (Stand: 8.7.2025) ausgewählt werden.
    - cycle_tracking_lutealphase.csv (Standard)
    - cycle_tracking_2025.csv (Testversion während der Programmierphase)

---

## ⚙️ Verwendete Versionen
- Python 3.11
- Streamlit 1.12

---

## 📁 Projektstruktur & Erklärung der Dateien

### Hauptverzeichnis

- **00_Dashboard.py**: Zentrale App-Oberfläche. Zyklusanalyse, Auswahl, Score & Planung.

### Source-Ordner

- **globals.py**: Initialisiert alle globalen Variablen & Objekte
- **classes.py**: Enthält Datenklassen: User, CyclePhase, SportSession
- **data_setup.py**: Lädt CSV-Daten & erzeugt Zyklusphasen und Einheiten
- **interface_components.py**: UI-Bausteine: Überschriften, Texte, Karten, Buttons
- **modules.py**: Interaktive Module: Auswahl, Score-Berechnung, Wochenplan
- **scores.py**: 	Rechenlogik zur Bewertung der Sportauswahl

---

## 🤖 KI-Verweis

KI wurde unterstützend eingesetzt, jedoch nicht zum automatisierten Coden der App.
Stattdessen diente sie zur strukturellen Optimierung, Dokumentation und Code-Aufräumung im späteren Entwicklungsprozess.