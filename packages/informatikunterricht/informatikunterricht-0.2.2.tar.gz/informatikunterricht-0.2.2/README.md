# Informatikunterricht - Bildverarbeitungsmodul und Visualisierung von Verteilungen
![Bildbeschreibung](https://raw.githubusercontent.com/henningmattes/diverse/main/csedu_package_img_small.png)

## Beschreibung

Dieses Projekt besteht aus zwei Modulen für den Informatikunterricht:

- **Bildverarbeitung**: Ein Modul zur einfachen Bearbeitung und Analyse von Bildern. Es ermöglicht das Laden, Speichern und Anzeigen von Bildern, die Berechnung von Farbtiefen und die Umwandlung von palettenbasierten Bildern in RGB. 

- **Visualisierung von Verteilungen**: Ein Modul zur Visualisierung von zwei Verteilungen nebeneinander als Linien- oder Balkendiagramme. Ideal zur Darstellung von statistischen Daten im Unterricht.

## Module

### bildverarbeitung

Dieses Modul bietet Funktionen für die einfache Verarbeitung und Analyse von Bildern. Die Hauptfunktionen sind:

- `lade_bild(pfad_und_dateiname)`: Lädt ein Bild und berechnet dessen Farbtiefe.
- `transformiere_palettenbild_zu_rgb(np_array_bild, palette)`: Transformiert ein palettenbasiertes Bild in ein RGB-Bild.
- `pillow_bild(numpy_array, palette=None)`: Konvertiert ein NumPy-Array in ein Pillow-Bild.
- `speichere_bild(pfad, np_array_bild, palette=None)`: Speichert ein Bild in einer Datei.
- `zeige(bilddaten, zeige_achsen=True, beschriftungsdaten=None, palettendaten=None, zeige_grid=False, grid_color='black', tickanzahl=None, spaltenanzahl=1, figsize=None)`: Zeigt Bilder in einem Plot an.
- `plot_histogramm(histogramm, palette='inferno')`: Plottet ein Histogramm der Helligkeitswerte eines Bildes.

### diagramme

Dieses Modul bietet eine einfache Möglichkeit zur Visualisierung von zwei Verteilungen. Die Hauptfunktion ist:

- `zeige_verteilungen(verteilung1, verteilung2, titel1="", titel2="", modus="Linien")`: Visualisiert zwei Verteilungen als Linien- oder Balkendiagramme.

## Beispielverwendung

### Bildverarbeitung

```python
from bildverarbeitung import lade_bild, zeige, speichere_bild

# Bild laden und Farbtiefe berechnen
bild, farbmodus, farbtiefe, palette = lade_bild('pfad/zum/bild.png')
print(f"Farbtiefe: {farbtiefe} Bit")

# Bild anzeigen
zeige(bild)

# Bild speichern
speichere_bild('pfad/zum/ausgabebild.png', bild, palette)

```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) with additional terms for attribution. See the [LICENSE](https://raw.githubusercontent.com/henningmattes/diverse/main/LICENSE.txt) file for details.
