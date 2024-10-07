"""
Informatikunterricht - Visualisierung von Verteilungen

Dieses Modul bietet Funktionen zur Visualisierung von zwei Verteilungen, die typischerweise
im Rahmen des Informatikunterrichts verwendet werden können. Es verwendet Matplotlib, um 
zwei Verteilungen nebeneinander als Linien- oder Balkendiagramme darzustellen. 

Funktionen:
- zeige_verteilungen(verteilung1, verteilung2, titel1="", titel2="", modus="Linien", figsize=(10, 10)):
    Visualisiert zwei Verteilungen als Linien- oder Balkendiagramme.

Parameter:
- verteilung1: Eine Liste oder ein Array, das die erste Verteilung darstellt.
- verteilung2: Eine Liste oder ein Array, das die zweite Verteilung darstellt.
- titel1: Titel für das erste Diagramm (Standard: leer).
- titel2: Titel für das zweite Diagramm (Standard: leer).
- modus: Modus der Darstellung, entweder "Linien" (Standard) oder "Balken".
- figsize: Höhe und Breite der Gesamtdarstellung.

Beispielverwendung:
    verteilung1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    verteilung2 = [26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    zeige_verteilungen(verteilung1, verteilung2, "Verteilung 1", "Verteilung 2", "Balken")

Hinweis:
Dieses Modul wurde speziell für den Einsatz im Informatikunterricht entwickelt und bietet 
eine einfache Möglichkeit, grundlegende Datenvisualisierungen durchzuführen. Es kann in 
anderen Projekten wiederverwendet werden, die ähnliche Anforderungen an die Visualisierung 
stellen.

Autor:
- Henning Mattes

Lizenz:
- MIT License mit Zusatz: Siehe LICENSE-Datei im Repository

Abhängigkeiten:
- matplotlib

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def zeige_verteilungen(verteilung1, verteilung2, titel1 = "", titel2 = "", modus = "Linien", figsize=(10, 10)):
    
    def zeichen(code26zahl):
        return chr(code26zahl + ord("A"))
    
    fig, axs = plt.subplots(2, 1, figsize=figsize)
    ticks = range(1, 27)
    beschriftungen = [zeichen(i-1) for i in ticks]
    for ax, verteilung, titel, color in zip(axs, [verteilung1, verteilung2], [titel1, titel2], ["red", "blue"]):
        if modus.upper() == "BALKEN":
            ax.bar(ticks, verteilung, align = 'center', color = color)
        else:
            ax.plot(ticks, verteilung, marker = "x", color = color)
        ax.grid()
        ax.set_xticks(ticks)
        ax.set_xticklabels(beschriftungen)
        ax.set_title(titel)
    plt.show()



def zeige_histogramme(histogramme, palettendaten='inferno', beschriftungsdaten=None, zeige_grid=False, grid_color='black', tickanzahl=None, titel_schriftgroesse=None, zahlen_schriftgroesse=None, spaltenanzahl=1, figsize=None):
    if not isinstance(histogramme, list):
        histogramme = [histogramme]  # Einzelnes Histogramm in Liste umwandeln
    
    def parameter_liste_vorbereiten(param, name, length):
        if isinstance(param, list):
            if len(param) != length:
                raise ValueError(f"Wenn für histogramme eine Liste übergeben wird, kann (muss aber nicht) auch für '{name}' eine"
                                 + f"Liste übergeben werden. In diesem Fall muss die Länge der Liste '{name}' der Länge der"
                                 + f" Liste histogramme entsprechen.")
        else:
            param = [param] * length
        return param

    palettendaten = parameter_liste_vorbereiten(palettendaten, 'palettendaten', len(histogramme))
    beschriftungsdaten = parameter_liste_vorbereiten(beschriftungsdaten, 'beschriftungsdaten', len(histogramme))
    zeige_grid = parameter_liste_vorbereiten(zeige_grid, 'zeige_grid', len(histogramme))
    grid_color = parameter_liste_vorbereiten(grid_color, 'grid_color', len(histogramme))
    tickanzahl = parameter_liste_vorbereiten(tickanzahl, 'tickanzahl', len(histogramme))
    titel_schriftgroesse = parameter_liste_vorbereiten(titel_schriftgroesse, 'titel_schriftgroesse', len(histogramme))
    zahlen_schriftgroesse = parameter_liste_vorbereiten(zahlen_schriftgroesse, 'zahlen_schriftgroesse', len(histogramme))

    anzahl_histogramme = len(histogramme)
    zeilenanzahl = np.ceil(anzahl_histogramme / spaltenanzahl).astype(int)

    # Dynamische Anpassung der figsize, falls nicht explizit angegeben
    if figsize is None:
        # Standardmäßige Gesamtbreite von Matplotlib herausfinden
        default_figsize = plt.rcParams["figure.figsize"]
        default_width = default_figsize[0]  # Standardbreite für eine Matplotlib-Figur
        
        # Proportionale Höhe für jedes Histogramm basierend auf der Breite
        individual_width = default_width / spaltenanzahl  # Breite pro Subplot
        # Höhe so setzen, dass sie geringer als die Breite ist, z.B. 4:3 Verhältnis
        individual_height = individual_width * (3 / 4)
        
        # Berechne die Gesamtgröße der Abbildung
        figsize = (default_width, zeilenanzahl * individual_height)

    fig, axs = plt.subplots(zeilenanzahl, spaltenanzahl, figsize=figsize)
    axs = np.ravel([axs])

    for idx, histogramm in enumerate(histogramme):
        ax = axs[idx]

        # Min und Max für die Normalisierung finden
        non_zero_values = histogramm[np.nonzero(histogramm)]
        if non_zero_values.size == 0:
            min_val = 0
        else:
            min_val = non_zero_values.min()
        max_val = histogramm.max()

        # Normalisierungsobjekt erstellen
        norm = Normalize(vmin=min_val, vmax=max_val)
        cmap = plt.get_cmap(palettendaten[idx])
        
        # ScalarMappable für die Colorbar
        mappable = ScalarMappable(norm=norm, cmap=cmap)

        # Balken zeichnen
        for i in range(256):
            color = cmap(0) if histogramm[i] == 0 else cmap(norm(histogramm[i]))
            ax.bar(i, histogramm[i], color=color, width=1)

        # Titel hinzufügen
        if beschriftungsdaten[idx] is not None:
            if titel_schriftgroesse[idx] is not None:
                ax.set_title(beschriftungsdaten[idx], fontsize=titel_schriftgroesse[idx])
            else:
                ax.set_title(beschriftungsdaten[idx])

        ax.set_xlim(0, 255)
        ax.set_ylim(0, max(histogramm) + max(histogramm) * 0.05)

        # X- und Y-Achsen-Ticks
        ax.set_xticks(range(0, 256, 50))
        y_ticks_max = max(histogramm) + 1
        ax.set_yticks(np.linspace(0, y_ticks_max, num=5, endpoint=True))
        
        # Tick-Anzahl für x- und y-Achsen anpassen
        if tickanzahl[idx] is not None:
            ax.set_xticks(np.linspace(0, 255, tickanzahl[idx], dtype=int))
            ax.set_yticks(np.linspace(0, y_ticks_max, tickanzahl[idx], dtype=int))

        if zahlen_schriftgroesse[idx] is not None:
            ax.tick_params(axis='both', which='major', labelsize=zahlen_schriftgroesse[idx])

        ax.set_xlabel('Helligkeit/Luminanzwerte (0-255)')
        ax.set_ylabel('Anzahl der Pixel')

        # Grid anzeigen
        if zeige_grid[idx]:
            ax.grid(True, color=grid_color[idx])
        else:
            ax.grid(False)

        # Colorbar hinzufügen
        cbar = ax.figure.colorbar(mappable, ax=ax)
        cbar.set_label('Anzahl der Pixel')

    plt.tight_layout()
    plt.show()
