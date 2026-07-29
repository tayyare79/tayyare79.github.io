# tayyare79.github.io

Landingpage und Support-Seiten für die iOS-/macOS-Apps von Harun Nakas.

Live: https://tayyare79.github.io

## Aufbau

- `index.html` – Landingpage mit allen Apps
- `support/` – Support-Übersicht
- `<app-slug>/` – Support- und Datenschutzseite je App
- `assets/style.css` – gemeinsames Stylesheet
- `build.py` – Generator; erzeugt alle HTML-Seiten aus dem App-Katalog

## Ändern

App-Katalog und FAQ-Texte stehen in `build.py`. Nach einer Änderung:

```bash
python3 build.py
git commit -am "Update" && git push
```

GitHub Pages liefert den `main`-Branch direkt aus – kein Build-Schritt nötig,
deshalb werden die erzeugten HTML-Dateien mit eingecheckt.

## Verwendet als

Support-URL und Datenschutz-URL in App Store Connect für die hier gelisteten Apps.
