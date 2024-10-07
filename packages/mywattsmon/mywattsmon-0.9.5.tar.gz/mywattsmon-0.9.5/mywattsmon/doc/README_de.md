# **mywattsmon**

Eine minimale Python-Applikation zur Überwachung von elektrischer Leistung und Energie im Smarthome.

- Unterstützung von Geräten wie Energiezähler, Schaltsteckdosen etc.
- 24/7 Monitorprozess mit Datenspeicherung nach Zeitplan
- Optionales Monitorfenster
- Geringer Ressourcenbedarf
- Leicht konfigurierbar via JSON-Datei
- Erweiterbar durch eigene Geräte-Klassen

Vorausgesetzt wird ein Rechner, auf dem Python ab Version 3.11 läuft. Für SBCs wie Raspberry Pi ist eine Festplatte (beispielsweise eine USB-SSD) zu empfehlen, da SD-Karten für den Dauerbetrieb im Allgemeinen nicht geeignet sind.

## Installieren

Die Applikation sollte in ein Benutzerverzeichnis installiert werden, da sie Daten speichert und individuell erweitert werden kann.

	python -m pip install mywattsmon -U -t <Zielverzeichnis> 

Alternativ kann die Release-Datei vom Repository heruntergeladen und entpackt werden.

## Anwenden

Im Folgenden wird angenommen, dass die Applikation auf einem Linux-Computer in das Home-Verzeichnis des Benutzers installiert wurde (beispielsweise in /home/u1/mywattsmon), und dass die Aufrufe vom Home-Verzeichnis aus erfolgen (/home/u1).

Den Monitorprozess starten (beenden mit Ctrl+C):

	python -m mywattsmon.app.monitor
    
Das Monitorfenster starten (beenden mit Ctrl+C, im Fenster per Exit-Button oder Escape-Taste):

	python -m mywattsmon.app.window

*Hinweis: Beim ersten Start der Applikation wird das Datenverzeichnis mywattsmon-data parallel zum Applikationsverzeichnis erstellt. Darin ist unter anderem die Konfigurationsdatei config.json mit einer Konfiguration der Geräteklasse Mock enthalten. Da diese Klasse Zufallszahlen liefert, ist die Applikation direkt nach der Installation ohne weitere Konfiguration ausführbar.*

## Weitere Informationen

- Dokumentation: /mywattsmon/doc/*
- Repository: https://github.com/berryunit/mywattsmon
- Lizenz: MIT
