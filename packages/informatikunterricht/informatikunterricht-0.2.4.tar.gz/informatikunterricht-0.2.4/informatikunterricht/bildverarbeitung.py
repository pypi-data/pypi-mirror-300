"""
Informatikunterricht - Bildverarbeitungsmodul

Dieses Modul bietet Funktionen für die sehr einfache erarbeitung und Analyse von Bildern.
Es ermöglicht das Laden, Speichern und Anzeigen von Bildern, sowie die Berechnung von
Farbtiefen und die Transformation von palettenbasierten Bildern in RGB.

Autor:
- Henning Mattes

Lizenz:
- MIT License mit Zusatz: Siehe LICENSE-Datei im Repository

Abhängigkeiten:
- numpy
- matplotlib
- pillow

Beispielverwendung:

    # Bild laden und Farbtiefe berechnen
    bild, farbmodus, farbtiefe, palette = lade_bild('pfad/zum/bild.png')
    print(f"Farbtiefe: {farbtiefe} Bit")

    # Bild anzeigen
    zeige(bild)

    # Bild speichern
    speichere_bild('pfad/zum/ausgabebild.png', bild, palette)

"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib import colormaps

def numpy_array(bild):
    original_farbmodus = bild.mode
    return (np.array(bild), original_farbmodus)

# Funktion zur Berechnung der Farbtiefe
def berechne_farbtiefe(bild):
    farbmodus = bild.mode
    if farbmodus == '1':  # Binärmodus
        return 1
    elif farbmodus == 'L':  # 8-Bit-Graustufen
        return 8
    elif farbmodus == 'RGB':  # 24-Bit-Farbe
        return 24
    elif farbmodus == 'RGBA':  # 32-Bit-Farbe mit Alpha
        return 32
    elif farbmodus == 'P':  # Palette
        palette = bild.getpalette()
        anzahl_farben = len({tuple(palette[i:i+3]) for i in range(0, len(palette), 3)})
        if anzahl_farben <= 16:
            return 4  # 4 Bits für 16 Farben
        else:
            return 8  # 8 Bits für mehr als 16 Farben
    else:
        return 'Unbekannt'

def transformiere_palettenbild_zu_rgb(np_array_bild, palette):
    # Erstellen eines leeren Bildes mit der gleichen Größe wie das Eingabebild
    bild = np.zeros((np_array_bild.shape[0], np_array_bild.shape[1], 3), dtype=np.uint8)
    
    # Ersetzen der Farbwerte durch die Werte aus der Palette
    for i in range(np_array_bild.shape[0]):
        for j in range(np_array_bild.shape[1]):
            bild[i, j] = palette[np_array_bild[i, j]]
    
    return bild

def lade_bild(pfad_und_dateiname):
    pil_bild = Image.open(pfad_und_dateiname)
    bild, farbmodus = numpy_array(pil_bild)
    if farbmodus == 'P':  # Palette
        palette = pil_bild.getpalette()
        # Umwandeln der flachen Palette in ein 2D-NumPy-Array (N x 3), wobei N die Anzahl der Farben ist
        palette_array = np.array(palette).reshape((-1, 3))
    else:
        palette_array = None
    return bild, farbmodus, berechne_farbtiefe(pil_bild), palette_array

def pillow_bild(numpy_array, palette=None):
    # Bestimmen des Farbmodus basierend auf der Form und der Palette
    if palette is not None:
        farbmodus = 'P'
        image = Image.fromarray(numpy_array.astype('uint8'), 'P')
        flat_palette = palette.flatten().tolist()
        image.putpalette(flat_palette)
    elif numpy_array.ndim == 2:
        farbmodus = 'L'
        image = Image.fromarray(numpy_array, 'L')
    elif numpy_array.shape[2] == 3:
        farbmodus = 'RGB'
        image = Image.fromarray(numpy_array, 'RGB')
    elif numpy_array.shape[2] == 4:
        farbmodus = 'RGBA'
        image = Image.fromarray(numpy_array, 'RGBA')
    else:
        raise ValueError("Unbekanntes Format oder Farbmodus kann nicht bestimmt werden")

    return image

def speichere_bild(pfad, np_array_bild, palette=None):
    # Erstellen des Pillow-Bildes, jetzt mit möglicher Palette
    pillow_image = pillow_bild(np_array_bild, palette)
    # Speichern des Bildes
    pillow_image.save(pfad)

def transformiere_palettenbild_zu_rgb(np_array_bild, palette):
    # Erstellen eines leeren Bildes mit der gleichen Größe wie das Eingabebild
    bild = np.zeros((np_array_bild.shape[0], np_array_bild.shape[1], 3), dtype=np.uint8)
    
    # Ersetzen der Farbwerte durch die Werte aus der Palette
    for i in range(np_array_bild.shape[0]):
        for j in range(np_array_bild.shape[1]):
            bild[i, j] = palette[np_array_bild[i, j]]
    
    return bild

def zeige(
    bilddaten,
    zeige_achsen=True,
    beschriftungsdaten=None,
    palettendaten=None,
    zeige_grid=False,
    grid_color='black',
    tickanzahl=None,
    titel_schriftgroesse=None,
    achsen_schriftgroesse=None,
    spaltenanzahl=1,
    figsize=None,
    zeige_zahlen=False,
    zahlen_schriftgroesse=None,
    zahlen_farbe=[0, 0, 0]
):
    """
    Zeigt eine oder mehrere Bilder mit verschiedenen Anzeigeoptionen.

    Die meisten Parameter können entweder als einzelner Wert oder als Liste von Werten übergeben werden.
    Wenn ein einzelner Wert übergeben wird, wird er auf alle Bilder angewendet.

    Parameters:
        bilddaten (list or np.ndarray): Liste der Bilder oder ein einzelnes Bild.
        zeige_achsen (bool or list of bool, optional): Ob die Achsen angezeigt werden sollen.
        beschriftungsdaten (list or single value, optional): Liste der Titel für die Bilder.
        palettendaten (list, str oder np.ndarray, optional): Farbpalette oder Colormap für die Bilder.
        zeige_grid (bool or list of bool, optional): Ob ein Raster angezeigt werden soll.
        grid_color (str or list of str, optional): Farbe des Rasters.
        tickanzahl (int or list of int, optional): Anzahl der Tick-Marken auf den Achsen.
        titel_schriftgroesse (int or list of int, optional): Schriftgröße der Titel.
        achsen_schriftgroesse (int or list of int, optional): Schriftgröße der Achsenbeschriftungen.
        spaltenanzahl (int, optional): Anzahl der Spalten in der Anzeige.
        figsize (tuple, optional): Größe der gesamten Abbildung.
        zeige_zahlen (bool or list of bool, optional): Ob Zahlen in den Bildfeldern angezeigt werden sollen.
        zahlen_schriftgroesse (int or list of int, optional): Schriftgröße der Zahlen.
        zahlen_farbe (list, tuple oder str, optional): Farbe der Zahlen. Kann als einzelner Wert oder Liste/Tupel übergeben werden.
            Falls als Tupel mit 3 int-Werten im Bereich 0-255 übergeben, werden diese automatisch auf 0-1 normalisiert.

    Example:
        ```python
        zeige(
            kernels_int,
            spaltenanzahl=2,
            palettendaten='Blues_r',
            figsize=(4, 4),
            zeige_zahlen=True,
            zahlen_farbe=(255, 255, 100)  # Wird automatisch zu (1.0, 1.0, 0.392) normalisiert
        )
        ```
    """
    if not isinstance(bilddaten, list):
        bilddaten = [bilddaten]  # Einzelbild in Liste umwandeln für einheitliche Verarbeitung

    def parameter_liste_vorbereiten(param, name, length):
        if isinstance(param, list):
            if len(param) != length:
                raise ValueError(
                    f"Wenn für bilddaten eine Liste übergeben wird, kann (muss aber nicht) auch für '{name}' eine "
                    f"Liste übergeben werden. In diesem Fall muss die Länge der Liste '{name}' der Länge der "
                    f"Liste bilddaten entsprechen."
                )
        elif isinstance(param, tuple) and name == 'zahlen_farbe' and len(param) == 3:
            # Für RGB-Tupel
            param = [param] * length
        else:
            param = [param] * length
        return param

    # Spezielle Behandlung für RGB-Wert oder Farbnamen (zahlen_farbe)
    if isinstance(zahlen_farbe, str):
        # Wenn es sich um einen String (Farbname) handelt, wende ihn auf alle Bilder an
        zahlen_farbe = [zahlen_farbe] * len(bilddaten)
    elif isinstance(zahlen_farbe, (list, tuple)) and len(zahlen_farbe) == 3 and all(isinstance(x, (int, float)) for x in zahlen_farbe):
        # Wenn es sich um einen RGB-Wert (Liste oder Tupel der Länge 3) handelt, wende ihn auf alle Bilder an
        zahlen_farbe = [zahlen_farbe] * len(bilddaten)
        # Überprüfen, ob die Werte im Bereich 0-255 sind und normalisieren, wenn ja
        for i in range(len(zahlen_farbe)):
            if all(isinstance(x, int) and 0 <= x <= 255 for x in zahlen_farbe[i]):
                zahlen_farbe[i] = tuple([x / 255.0 for x in zahlen_farbe[i]])

    # Parameterlisten vorbereiten
    palettendaten = parameter_liste_vorbereiten(palettendaten, 'palettendaten', len(bilddaten))
    beschriftungsdaten = parameter_liste_vorbereiten(beschriftungsdaten, 'beschriftungsdaten', len(bilddaten))
    zeige_grid = parameter_liste_vorbereiten(zeige_grid, 'zeige_grid', len(bilddaten))
    grid_color = parameter_liste_vorbereiten(grid_color, 'grid_color', len(bilddaten))
    tickanzahl = parameter_liste_vorbereiten(tickanzahl, 'tickanzahl', len(bilddaten))
    titel_schriftgroesse = parameter_liste_vorbereiten(titel_schriftgroesse, 'titel_schriftgroesse', len(bilddaten))
    achsen_schriftgroesse = parameter_liste_vorbereiten(achsen_schriftgroesse, 'achsen_schriftgroesse', len(bilddaten))
    zeige_zahlen = parameter_liste_vorbereiten(zeige_zahlen, 'zeige_zahlen', len(bilddaten))
    zahlen_schriftgroesse = parameter_liste_vorbereiten(zahlen_schriftgroesse, 'zahlen_schriftgroesse', len(bilddaten))
    zahlen_farbe = parameter_liste_vorbereiten(zahlen_farbe, 'zahlen_farbe', len(bilddaten))

    anzahl_bilder = len(bilddaten)
    zeilenanzahl = int(np.ceil(anzahl_bilder / spaltenanzahl))

    # Erstelle Subplots
    if figsize is None:
        figsize = (spaltenanzahl * 5, zeilenanzahl * 5)
    fig, axs = plt.subplots(zeilenanzahl, spaltenanzahl, figsize=figsize)
    
    # Handhabung der axs-Struktur
    if anzahl_bilder == 1:
        axs = np.array([axs])
    else:
        axs = axs.flatten()

    for idx, bild in enumerate(bilddaten):
        ax = axs[idx]

        # Titel einstellen
        if beschriftungsdaten[idx] is not None:
            if titel_schriftgroesse[idx] is not None:
                ax.set_title(beschriftungsdaten[idx], fontsize=titel_schriftgroesse[idx])
            else:
                ax.set_title(beschriftungsdaten[idx])

        # Bild darstellen
        current_palette = palettendaten[idx]
        if isinstance(current_palette, np.ndarray):
            bild_rgb = transformiere_palettenbild_zu_rgb(bild, current_palette)
            ax.imshow(bild_rgb)
        else:
            cmap = current_palette if current_palette is not None else 'gray'
            ax.imshow(bild, cmap=cmap)

        # Achsen anzeigen
        if zeige_achsen:
            ax.axis('on')
            if achsen_schriftgroesse[idx] is not None:
                ax.tick_params(axis='both', which='major', labelsize=achsen_schriftgroesse[idx])

            if tickanzahl[idx] is not None:
                ticks_x = np.linspace(0, bild.shape[1] - 1, num=tickanzahl[idx], dtype=int)
                ticks_y = np.linspace(0, bild.shape[0] - 1, num=tickanzahl[idx], dtype=int)
                ax.set_xticks(ticks_x)
                ax.set_yticks(ticks_y)
                ax.set_xticklabels(ticks_x)
                ax.set_yticklabels(ticks_y)
        else:
            ax.axis('off')

        # Raster anzeigen
        if zeige_grid[idx]:
            ax.set_xticks(np.arange(-.5, bild.shape[1], 1), minor=True)
            ax.set_yticks(np.arange(-.5, bild.shape[0], 1), minor=True)
            ax.grid(which="minor", color=grid_color[idx], linestyle='-', linewidth=1)
            ax.tick_params(which="minor", size=0)
        else:
            ax.grid(False)

        # Zahlen in Feldern anzeigen
        if zeige_zahlen[idx]:
            for i in range(bild.shape[0]):
                for j in range(bild.shape[1]):
                    wert = bild[i, j]
                    if isinstance(wert, (np.ndarray, list)):
                        # Für RGB-Werte
                        wert = tuple(map(int, wert))  # Umwandeln in ein Tupel mit Integer-Werten
                        text = f"{wert}"
                    else:
                        # Für skalare Werte: Dynamische Formatierung
                        if isinstance(wert, float) and not wert.is_integer():
                            text = f"{wert:.2f}".rstrip('0').rstrip('.')
                        else:
                            text = f"{int(wert)}"
                    ax.text(
                        j, i, text,
                        ha="center", va="center",
                        color=zahlen_farbe[idx],
                        fontsize=(zahlen_schriftgroesse[idx] if zahlen_schriftgroesse[idx] is not None else None)
                    )

    plt.tight_layout()
    plt.show()


def erzeuge_bild_aus_farbkanaelen(farbkanal_rot = None, farbkanal_gruen = None, farbkanal_blau = None):
    bild_array = None
    dim_x = 0
    dim_y = 0
    if not farbkanal_rot is None:
        dim_x, dim_y = farbkanal_rot.shape
        bild_array = np.empty([dim_x, dim_y, 3], dtype=np.uint8)
        bild_array[:, :, 0] = farbkanal_rot
    if not (farbkanal_gruen is None):
        if bild_array is None:
            dim_x, dim_y = farbkanal_gruen.shape
            bild_array = np.empty([dim_x, dim_y, 3], dtype=np.uint8)
        else:
            if dim_x != farbkanal_gruen.shape[0] or dim_y != farbkanal_gruen.shape[1]:
                raise ValueError("Dimensionen der Farbkanäle stimmen nicht überein")
        bild_array[:, :, 1] = farbkanal_gruen
    if not (farbkanal_blau is None):
        if bild_array is None:
            dim_x, dim_y = farbkanal_blau.shape
            bild_array = np.empty([dim_x, dim_y, 3], dtype=np.uint8)
        else:
            if dim_x != farbkanal_blau.shape[0] or dim_y != farbkanal_blau.shape[1]:
                raise ValueError("Dimensionen der Farbkanäle stimmen nicht überein")
        bild_array[:, :, 2] = farbkanal_blau
    return bild_array


def fuege_padding_hinzu(bild_array, pad_height, pad_width, padding_mode='constant', pad_value=128):
    # Höhe und Breite des Originalbildes
    bild_height, bild_width = bild_array.shape

    # Neues Bild mit Padding-Größe erstellen
    if padding_mode == 'constant':
        bild_mitRand = np.full((bild_height + 2 * pad_height, bild_width + 2 * pad_width), pad_value, dtype=np.uint8)
    else:
        bild_mitRand = np.zeros((bild_height + 2 * pad_height, bild_width + 2 * pad_width))

    # Originalbild in das neue Bild einfügen
    start_y, end_y = pad_height, pad_height + bild_height
    start_x, end_x = pad_width, pad_width + bild_width
    bild_mitRand[start_y:end_y, start_x:end_x] = bild_array
    
    # Verschiedene Padding-Modi anwenden
    if padding_mode == 'reflect':
        # Oben und unten
        for y in range(pad_height):
            bild_mitRand[y, pad_width:pad_width+bild_width] = bild_array[pad_height-1-y, :]
            bild_mitRand[pad_height+bild_height+y, pad_width:pad_width+bild_width] = bild_array[bild_height-y-1, :]

        # Links und rechts
        for x in range(pad_width):
            bild_mitRand[pad_height:pad_height+bild_height, x] = bild_mitRand[pad_height:pad_height+bild_height, pad_width*2-x-1]
            bild_mitRand[pad_height:pad_height+bild_height, pad_width+bild_width+x] = bild_mitRand[pad_height:pad_height+bild_height, pad_width+bild_width-x-2]

    elif padding_mode == 'edge':
        # Oben und unten
        for y in range(pad_height):
            bild_mitRand[y, pad_width:pad_width+bild_width] = bild_array[0, :]
            bild_mitRand[pad_height+bild_height+y, pad_width:pad_width+bild_width] = bild_array[-1, :]

        # Links und rechts
        for x in range(pad_width):
            bild_mitRand[pad_height:pad_height+bild_height, x] = bild_mitRand[pad_height:pad_height+bild_height, pad_width]
            bild_mitRand[pad_height:pad_height+bild_height, pad_width+bild_width+x] = bild_mitRand[pad_height:pad_height+bild_height, pad_width+bild_width-1]

    return bild_mitRand


def filtere(bild_array, kernel, negative_werte = 'normalisieren'):

    def normalisiere_bild(bild):
        """
        Normalisiert das Bild, indem die Werte auf den Bereich 0 bis 255 skaliert werden.
        """
        min_wert = bild.min()
        max_wert = bild.max()
        normalisiert = (bild - min_wert) / (max_wert - min_wert) * 255
        return normalisiert.astype(np.uint8)

    def verschiebe_farben(bild):
        """
        Verschiebt die Bildwerte, sodass alle Werte positiv sind, und skaliert auf den Bereich 0 bis 255.
        """
        verschoben = bild + abs(bild.min())
        max_wert = verschoben.max()
        verschoben = (verschoben / max_wert) * 255
        return verschoben.astype(np.uint8)

    (kernel_hoehe, kernel_breite) = kernel.shape
    (bild_hoehe, bild_breite) = bild_array.shape
    
    # Ergebnis-Array initialisieren
    gefiltertes_bild = np.zeros(shape = (bild_hoehe - (kernel_hoehe-1), bild_breite - (kernel_breite-1)), dtype=np.float64)

    # Faltung mit geschachtelten for-Schleifen
    for y in range(0, gefiltertes_bild.shape[0]):
        for x in range(0, gefiltertes_bild.shape[1]):
            # Teil des Bildes auswählen, der dem Kernel entspricht
            teil = bild_array[y:y+kernel_hoehe, x:x+kernel_breite]
            # Faltung: Elementweise Multiplikation und Summierung
            gefiltertes_bild[y, x] = np.sum(teil * kernel)

    # Negative Werte normalisieren oder verschieben, wenn gewünscht
    if negative_werte == 'normalisieren':
        if np.min(kernel)<0:
            gefiltertes_bild = normalisiere_bild(gefiltertes_bild)
    elif negative_werte == 'verschieben':
        if np.min(kernel)<0:
            gefiltertes_bild = verschiebe_farben(gefiltertes_bild)
    else:
        return gefiltertes_bild
    
    return gefiltertes_bild.astype(np.uint8)

def wandle_um_in_rgb(array_2dim, palette):
    # Broadcasting: Verwende die Graustufen-Werte als Indizes, um die Palette auf das RGB-Bild zu übertragen
    return palette[array_2dim]

def wandle_um_in_graustufen_bild(rgbArray):
    # Rec. 709 - Gewichtung
    r = rgbArray[:, :, 0]
    g = rgbArray[:, :, 1]
    b = rgbArray[:, :, 2]
    luminanz = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminanz.astype(np.uint8)

def gib_farbpalette(name, n=256):
    mpl_palette = colormaps[name]
    # Alpha-Kanal weglassen und normiert auf [0, 1]
    normierte_palette = mpl_palette(np.linspace(0, 1, n))[:, :3]
    return (normierte_palette * 255).astype(np.uint8)  # Umwandlung in uint8

