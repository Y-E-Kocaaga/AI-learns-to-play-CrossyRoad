# KI lernt, wie man CrossyRoad spielt

## Einleitung
Dieses Projekt zielt darauf ab, eine KI zu trainieren, die eine vereinfachte Version des Spiels CrossyRoad spielen kann. Die Implementierung erfolgt in **Python**, wobei **Pygame** für das Spiel und **NEAT** für die KI verwendet werden.

## Spielmechanik
- Der Spieler wird als **rotes Quadrat** dargestellt und kann sich mit den Pfeiltasten bewegen.
- Das Spielfeld ist in ein **Gitter** eingeteilt, wobei sich der Spieler nur von Feld zu Feld bewegen kann.
- Das Level **scrollt nach oben**, sodass sich der Spieler schnell bewegen muss, um nicht vom Bildschirmrand überholt zu werden.
- Hindernisse sind **Autos**, die sich auf **Straßen** bewegen. Der Spieler darf diese nicht berühren.
- Die Punktzahl ergibt sich aus der Anzahl der Felder, die der Spieler in vertikaler Richtung überquert hat.

## KI-Implementierung
### Neat-Algorithmus
- Ein **genetischer Algorithmus**, der neuronale Netze generiert und deren Struktur optimiert.
- **Fitness-Werte** werden genutzt, um Netzwerke nach Leistung zu bewerten.
- Erfolgreiche Netzwerke werden kombiniert und mutiert, um immer bessere Spieler zu erzeugen.

### Inputs, Outputs und Fitness
- Inputs: Spielerposition, Abstand zu Autos, Entfernung zum Bildschirmrand.
- Outputs: Bewegung nach **links**, **rechts**, **oben**, **unten** oder **Stehenbleiben**.
- Fitness: Punkte erhöhen sich bei Fortschritt im Spiel, gute Taktiken werden belohnt.

## Herausforderungen und Ergebnisse
- Verschiedene **Input-Strategien** wurden getestet, darunter absolute Positionen und Differenzen zu Autos.
- Anpassungen der **Level-Generierung**, um bessere Vergleichbarkeit zu schaffen.
- Verwendung von **Sensoren** zur Umgebungserkennung führte nicht zu besseren Ergebnissen.
- **KI konnte keine menschlichen Spieler übertreffen** – neue Ansätze erforderlich.

## Bot-Entwicklung
Da die KI das Spiel nicht erfolgreich meistern konnte, wurde ein **Bot** programmiert, der:
- Entscheidungen im Voraus simuliert und sichere Wege berechnet.
- Theoretisch unendlich lange spielen kann.
- Punktzahlen von **über 30.000** erreicht.

## Fazit
- Der **NEAT-Algorithmus** war nicht erfolgreich für dieses Problem.
- **Komplexere Weg-Finde-Algorithmen** wären notwendig.
- Alternativ kann ein Bot das Spiel zuverlässig spielen.
