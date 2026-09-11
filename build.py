#!/usr/bin/env python3
"""Generiert die statischen Seiten dieser Website.

Aufruf:  python3 build.py
Ergebnis: index.html, support/index.html und je eine Seite pro App-Slug.
Die erzeugten Dateien werden mit eingecheckt, damit GitHub Pages sie direkt
ausliefern kann (kein Build-Schritt auf GitHub nötig).
"""

import os
import html

SITE = "https://tayyare79.github.io"
EMAIL = "harunnakas@gmail.com"
DEV = "Harun Nakas"

# --------------------------------------------------------------------------
# App-Katalog. `support` = eigener Slug auf dieser Site oder externe URL.
# --------------------------------------------------------------------------

APPS = [
    # Medizin & Praxis
    dict(slug="leichenschau", name="Leichenschau Abrechnung", asc_id="6762590878",
         group="Medizin & Praxis", platforms="iPhone · iPad · Mac",
         tag="Abrechnung",
         short="Ärztliche Leichenschau nach GOÄ abrechnen – Ziffern 100/101, "
               "Wegegeld nach §8, Zuschläge und Vordrucksatz, fertig als PDF.",
         local_data=True),
    dict(slug="goae", name="GOÄ Abrechnung", asc_id="6762179870",
         group="Medizin & Praxis", platforms="iPhone · iPad",
         tag="Abrechnung",
         short="Privatliquidation nach GOÄ: Ziffern, Faktoren, Notdienst-Zuschläge "
               "und Rechnungen als PDF – mit Patienten- und Rechnungsverwaltung.",
         local_data=True),
    dict(slug="schrauberguide", name="SchrauberGuide", asc_id="6790098631",
         group="Medizin & Praxis", platforms="iPhone",
         tag="Bald verfügbar", unreleased=True,
         short="Nachschlagewerk und Helfer für Schrauber-Projekte.",
         local_data=True),

    # Reise & Städte
    dict(slug="fethiye-app", name="Fethiye App", asc_id="6763344254",
         group="Reise & Städte", platforms="iPhone · iPad", tag="Reiseführer",
         short="Reiseführer für Fethiye und die Region Muğla: Orte, Strände, "
               "Restaurants und Touren."),
    dict(slug="fethiye-guide", name="Fethiye Guide", asc_id="6766074524",
         group="Reise & Städte", platforms="iPhone", tag="Reiseführer",
         short="Kompakter Guide für Fethiye mit Highlights und Tipps."),
    dict(slug="marmaris-app", name="Marmaris App", asc_id="6770888895",
         group="Reise & Städte", platforms="iPhone · iPad", tag="Reiseführer",
         short="Reiseführer für Marmaris: Sehenswürdigkeiten, Buchten, Gastronomie "
               "und Ausflüge."),
    dict(slug="fethiye-fly", name="Fethiye Fly", asc_id="6786614423",
         group="Reise & Städte", platforms="iPhone", tag="Bald verfügbar",
         unreleased=True,
         short="Gleitschirmflüge und Aktivitäten rund um Fethiye."),

    # Apps mit bereits funktionierender externer Supportseite
    dict(slug=None, name="Fethiye Travel", asc_id="6778738153",
         group="Reise & Städte", platforms="iPhone",
         tag="Reiseführer", support="https://fethiye-app.com/support/",
         short="Reise-App für Fethiye mit Karten und Empfehlungen."),
    dict(slug=None, name="Bodrum App", asc_id="6770546050",
         group="Reise & Städte", platforms="iPhone · iPad", tag="Reiseführer",
         support="https://tayyare79.github.io/bodrum-app-website/",
         short="Reiseführer für Bodrum und die Halbinsel."),
    dict(slug=None, name="Bodrum Guide", asc_id="6778738113",
         group="Reise & Städte", platforms="iPhone", tag="Reiseführer",
         support="https://fethiye-app.com/support/",
         short="Kompakter Guide für Bodrum."),
    dict(slug=None, name="Marmaris Guide", asc_id="6778738179",
         group="Reise & Städte", platforms="iPhone", tag="Reiseführer",
         support="https://fethiye-app.com/support/",
         short="Kompakter Guide für Marmaris."),

    # Hotels & Gastronomie
    dict(slug=None, name="Nakas Hotel", asc_id="6786472360",
         group="Hotels & Gastronomie", platforms="iPhone", tag="Hotel",
         support="https://nakashotel.com",
         short="Gäste-App des Nakas Hotel in Fethiye."),
    dict(slug=None, name="Nakas Suites", asc_id="6786721393",
         group="Hotels & Gastronomie", platforms="iPhone", tag="Hotel",
         support="https://tayyare79.github.io/nakas-suites/",
         short="Gäste-App der Nakas Suites."),
    dict(slug=None, name="La Farine Rooms", asc_id="6786478743",
         group="Hotels & Gastronomie", platforms="iPhone", tag="Hotel",
         support="https://www.lafarinerooms.com",
         short="Gäste-App des La Farine City Hotel in Fethiye."),
    dict(slug=None, name="La Farine Pizzeria", asc_id="6771307009",
         group="Hotels & Gastronomie", platforms="iPhone", tag="Gastronomie",
         support="https://www.instagram.com/lafarine.pizzeria",
         short="App der Pizzeria La Farine."),

    # Alltag
    dict(slug=None, name="Kalendera – Kalender & Termine", asc_id="6774502037",
         group="Alltag & Sonstiges", platforms="iPhone", tag="Produktivität",
         support="https://tayyare79.github.io/kalendera-support/",
         short="Kalender- und Termin-App mit Fokus auf schnelle Erfassung."),
    dict(slug=None, name="Booster Catch", asc_id="6789857812",
         group="Alltag & Sonstiges", platforms="iPhone", tag="Spiel",
         support="https://tayyare79.github.io/starship-catch-support/",
         short="Arcade-Spiel: Boosterlandung mit steigendem Schwierigkeitsgrad."),

    dict(slug="mathestart", name="MatheStart", asc_id="",
         group="Alltag & Sonstiges", platforms="iPhone · iPad",
         tag="Lernen", unreleased=True,
         short="Offline Mathe-Vorschule für 4–7: kurze Tagesrunden, Zählen, "
               "Formen und Mengen — ohne Werbung, ohne Tracking.",
         local_data=True),
]

GROUPS = ["Medizin & Praxis", "Reise & Städte", "Hotels & Gastronomie", "Alltag & Sonstiges"]

# --------------------------------------------------------------------------
# Support-Inhalte je App-Seite
# --------------------------------------------------------------------------

FAQ_COMMON = [
    ("Wo werden meine Daten gespeichert?",
     "Alle Eingaben bleiben auf Ihrem Gerät. Die App überträgt keine Inhalte an den "
     "Entwickler oder an Dritte."),
    ("Wie erreiche ich den Support?",
     f"Schreiben Sie an <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. Bitte nennen Sie "
     "Gerät, Betriebssystem-Version und App-Version – dann geht es schneller."),
    ("Wie finde ich die App-Version?",
     "Die Versionsnummer steht auf der Produktseite im App Store unterhalb von "
     "„Neue Funktionen“ sowie in den Einstellungen der App, sofern dort ein "
     "Info-Bereich vorhanden ist."),
]

FAQ_PURCHASE = [
    ("Ich habe Pro gekauft – wie stelle ich den Kauf auf einem neuen Gerät wieder her?",
     "Öffnen Sie den Pro-Bereich in der App und tippen Sie auf „Käufe "
     "wiederherstellen“. Wichtig ist, dass Sie mit derselben Apple-ID angemeldet "
     "sind, mit der Sie gekauft haben."),
    ("Ist der Kauf ein Abo?",
     "Nein. Pro ist ein einmaliger Kauf ohne laufende Kosten."),
    ("Ich habe die App früher als Bezahl-App gekauft – muss ich erneut zahlen?",
     "Nein. Wer die App vor der Umstellung auf das kostenlose Modell gekauft hat, "
     "behält den vollen Funktionsumfang automatisch. Falls die Freischaltung nicht "
     "greift, hilft „Käufe wiederherstellen“ – und andernfalls eine kurze E-Mail."),
]

APP_SUPPORT = {
    "leichenschau": dict(
        intro="Support und Datenschutz für die App <strong>Leichenschau Abrechnung</strong> "
              "(iPhone, iPad und Mac).",
        faq=[
            ("Welche Positionen sind hinterlegt?",
             "GOÄ-Ziffer 100 (vorläufige Todesfeststellung) und 101 (Todesfeststellung/"
             "Todesbescheinigung) jeweils mit Faktor 0,6 und 1,0, Wegegeld nach §8 GOÄ "
             "gestaffelt nach Entfernung und Tages-/Nachtzeit, die Zuschläge E, N, G und H, "
             "der Zuschlag Nr. 102 sowie der Vordrucksatz der Todesbescheinigung "
             "(Freistaat Bayern)."),
            ("Wie erzeuge ich die Abrechnung als PDF?",
             "Einsatz anlegen, Positionen antippen, in der Zusammenfassung auf "
             "„PDF-Vorschau öffnen“ tippen. Aus der Vorschau lässt sich das PDF teilen, "
             "sichern oder drucken."),
            ("Gilt mein Kauf auch auf dem Mac?",
             "Ja. iPhone-, iPad- und Mac-Version teilen sich denselben Kauf, solange "
             "dieselbe Apple-ID verwendet wird."),
            ("Sind die Beträge rechtsverbindlich?",
             "Nein. Die App ist eine Rechenhilfe. Gebührensätze können sich ändern – "
             "bitte prüfen Sie alle Angaben vor der Abrechnung eigenverantwortlich. "
             "Die App ersetzt keine rechtliche oder abrechnungsfachliche Beratung."),
        ] + FAQ_PURCHASE,
        privacy_extra="Erfasste Einsatzdaten – darunter der Name verstorbener Personen, "
                      "Kostenträger sowie Arztname und LANR – werden ausschließlich lokal "
                      "in der App-Datenbank auf Ihrem Gerät gespeichert. Erzeugte PDFs "
                      "legen Sie selbst über die Teilen-Funktion ab; erst dadurch verlassen "
                      "Daten die App.",
    ),
    "goae": dict(
        intro="Support und Datenschutz für die App <strong>GOÄ Abrechnung</strong>.",
        faq=[
            ("Wofür ist die App gedacht?",
             "Für die Privatliquidation nach GOÄ: Leistungsziffern auswählen, Faktoren "
             "und Begründungen erfassen, Rechnungen als PDF erzeugen und den "
             "Zahlungsstatus im Blick behalten."),
            ("Woher stammen die Beträge?",
             "Die Beträge werden aus den Punktzahlen der GOÄ mit dem gesetzlichen "
             "Punktwert berechnet. Trotz sorgfältiger Prüfung gilt: Die App ist eine "
             "Rechenhilfe und ersetzt keine abrechnungsfachliche Beratung – bitte "
             "prüfen Sie jede Rechnung vor dem Versand."),
            ("Kann ich meine Daten exportieren?",
             "Ja, Rechnungen lassen sich als PDF und die Übersicht als CSV-Datei "
             "exportieren. Der Export erfolgt über die Teilen-Funktion Ihres Geräts."),
        ] + FAQ_PURCHASE,
        privacy_extra="Patienten- und Rechnungsdaten werden ausschließlich lokal auf "
                      "Ihrem Gerät gespeichert. Eine gesetzte App-PIN wird nicht im "
                      "Klartext, sondern als Hashwert im Schlüsselbund des Geräts "
                      "abgelegt. Exportierte PDF- und CSV-Dateien speichern oder "
                      "versenden Sie selbst – erst dadurch verlassen Daten die App.",
    ),
    "schrauberguide": dict(
        intro="Support für die App <strong>SchrauberGuide</strong>.",
        faq=[],
    ),
    "fethiye-app": dict(
        intro="Support für die App <strong>Fethiye App</strong> – Reiseführer für "
              "Fethiye und die Region Muğla.",
        faq=[
            ("Funktioniert die App ohne Internet?",
             "Die Inhalte sind in der App enthalten. Für Karten, Routen und externe "
             "Links wird eine Internetverbindung benötigt."),
            ("Ein Ort hat geschlossen oder eine Angabe stimmt nicht mehr – was tun?",
             f"Schreiben Sie kurz an <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. "
             "Korrekturen fließen in das nächste Update ein."),
        ],
    ),
    "fethiye-guide": dict(
        intro="Support für die App <strong>Fethiye Guide</strong>.",
        faq=[
            ("Ein Ort hat geschlossen oder eine Angabe stimmt nicht mehr – was tun?",
             f"Schreiben Sie kurz an <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. "
             "Korrekturen fließen in das nächste Update ein."),
        ],
    ),
    "marmaris-app": dict(
        intro="Support für die App <strong>Marmaris App</strong> – Reiseführer für "
              "Marmaris und Umgebung.",
        faq=[
            ("Funktioniert die App ohne Internet?",
             "Die Inhalte sind in der App enthalten. Für Karten, Routen und externe "
             "Links wird eine Internetverbindung benötigt."),
            ("Ein Ort hat geschlossen oder eine Angabe stimmt nicht mehr – was tun?",
             f"Schreiben Sie kurz an <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. "
             "Korrekturen fließen in das nächste Update ein."),
        ],
    ),
    "fethiye-fly": dict(
        intro="Support für die App <strong>Fethiye Fly</strong>.",
        faq=[],
    ),
    "mathestart": dict(
        intro="Support und Datenschutz für die App <strong>MatheStart</strong> "
              "(offline Mathe-Vorschule für Kindergarten bis Schulstart).",
        faq=[
            ("Für welches Alter ist die App?",
             "Für Kinder von etwa 4 bis 7 Jahren (Kindergarten bis Schulstart). "
             "Der Elternbereich ist hinter einem Rechen-Gate."),
            ("Braucht die App Internet?",
             "Nein. Alle Spiele und der Fortschritt bleiben auf dem Gerät. "
             "Zahlen und kurze Anweisungen nutzt die App über die "
             "Apple-Sprachausgabe auf dem Gerät, nicht über die Cloud."),
            ("Gibt es ein Abo oder In-App-Käufe?",
             "In Version 1.0 nicht. Die App ist ohne StoreKit/IAP."),
        ],
        privacy_extra="Die optionale Sprachausgabe nutzt ausschließlich Apples "
                      "On-Device-TTS (AVSpeechSynthesizer). Es werden keine "
                      "Kinderstimmen oder Lernstände in die Cloud übertragen. "
                      "Version 1.0 enthält keine In-App-Käufe.",
    ),
}

# --------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------

def head(title, desc, depth):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="color-scheme" content="dark light">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="brand" href="{up}">{DEV} · Apps</a>
    <nav class="site">
      <a href="{up}#apps">Apps</a>
      <a href="{up}support/">Support</a>
      <a href="mailto:{EMAIL}">Kontakt</a>
    </nav>
  </div>
</header>
"""


def foot(depth):
    up = "../" * depth
    return f"""<footer class="site">
  <div class="wrap foot-row">
    <div>© {DEV} · Unabhängiger App-Entwickler</div>
    <div>
      <a href="{up}support/">Support</a> ·
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


def store_url(asc_id):
    return f"https://apps.apple.com/de/app/id{asc_id}"


def support_href(app, depth):
    """Support-Ziel einer App – eigene Seite oder externe URL."""
    up = "../" * depth
    if app.get("slug"):
        return f"{up}{app['slug']}/"
    return app["support"]


def write(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


# --------------------------------------------------------------------------
# Seiten
# --------------------------------------------------------------------------

def build_index():
    cards = []
    for group in GROUPS:
        apps = [a for a in APPS if a["group"] == group]
        if not apps:
            continue
        cards.append(f'<section id="{group.split()[0].lower()}"><div class="wrap">')
        cards.append(f"<h2>{html.escape(group)}</h2>")
        cards.append('<div class="grid">')
        for a in apps:
            store = "" if a.get("unreleased") else \
                f'<a href="{store_url(a["asc_id"])}">Im App Store</a>'
            cards.append(f"""  <article class="card">
    <span class="badge">{html.escape(a['tag'])}</span>
    <h3>{html.escape(a['name'])}</h3>
    <p>{a['short']}</p>
    <div class="links">
      {store}
      <a href="{support_href(a, 0)}">Support</a>
    </div>
  </article>""")
        cards.append("</div></div></section>")

    body = f"""<div class="hero">
  <div class="wrap">
    <h1>Apps von {DEV}</h1>
    <p class="lead">Praxis-Software für die ärztliche Abrechnung sowie Reise- und
    Gäste-Apps für die türkische Ägäis. Entwickelt für iPhone, iPad und Mac –
    ohne Werbung, ohne Tracking, mit Daten, die auf dem Gerät bleiben.</p>
    <div class="hero-actions">
      <a class="btn" href="#apps">Alle Apps ansehen</a>
      <a class="btn ghost" href="support/">Support &amp; Hilfe</a>
    </div>
  </div>
</div>

<section id="apps"><div class="wrap">
  <h2>Übersicht</h2>
  <p class="section-sub">Jede App hat eine eigene Supportseite mit häufigen Fragen,
  Datenschutzhinweisen und einer Kontaktadresse.</p>
</div></section>
{''.join(cards)}

<section id="kontakt"><div class="wrap">
  <h2>Kontakt</h2>
  <p class="section-sub">Fragen, Fehlermeldungen oder Wünsche für ein Update?
  Ich antworte in der Regel innerhalb von zwei Werktagen.</p>
  <p><a class="btn" href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>
"""
    write("index.html",
          head(f"{DEV} – Apps für iPhone, iPad und Mac",
               "Apps von Harun Nakas: ärztliche Abrechnung, Reiseführer und "
               "Gäste-Apps für iPhone, iPad und Mac.", 0)
          + body + foot(0))


def build_support_hub():
    rows = []
    for group in GROUPS:
        apps = [a for a in APPS if a["group"] == group]
        if not apps:
            continue
        rows.append(f"<h3>{html.escape(group)}</h3><ul>")
        for a in apps:
            rows.append(f'<li><a href="{support_href(a, 1)}">{html.escape(a["name"])}</a></li>')
        rows.append("</ul>")

    body = f"""<div class="page"><div class="wrap prose">
  <p class="kicker">Support</p>
  <h1>Hilfe zu meinen Apps</h1>
  <p>Wählen Sie unten die betreffende App – dort finden Sie häufige Fragen,
  Hinweise zum Datenschutz und die Kontaktmöglichkeit.</p>

  <div class="panel">
    <h3>Direkter Kontakt</h3>
    <p>Schreiben Sie an <a href="mailto:{EMAIL}">{EMAIL}</a>.
    Damit ich schnell helfen kann, nennen Sie bitte:</p>
    <ul>
      <li>Name der App und – falls bekannt – die Versionsnummer</li>
      <li>Gerät und Betriebssystem-Version (z.&nbsp;B. iPhone 15, iOS 18.5)</li>
      <li>eine kurze Beschreibung, was Sie getan haben und was passiert ist</li>
    </ul>
    <p>Ich antworte in der Regel innerhalb von zwei Werktagen.</p>
  </div>

  <h2>Apps</h2>
  {''.join(rows)}
</div></div>
"""
    write("support/index.html",
          head(f"Support – Apps von {DEV}",
               "Support und Hilfe zu allen Apps von Harun Nakas.", 1)
          + body + foot(1))


def build_app_page(app):
    slug = app["slug"]
    cfg = APP_SUPPORT[slug]
    faq = cfg["faq"] + FAQ_COMMON

    faq_html = "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq
    )

    store_block = ""
    if not app.get("unreleased"):
        store_block = (f'<p><a class="btn" href="{store_url(app["asc_id"])}">'
                       f'Im App Store ansehen</a></p>')

    privacy_extra = cfg.get("privacy_extra", "")
    privacy_extra_html = f"<p>{privacy_extra}</p>" if privacy_extra else ""

    body = f"""<div class="page"><div class="wrap prose">
  <p class="kicker">Support</p>
  <h1>{html.escape(app['name'])}</h1>
  <p>{cfg['intro']}</p>
  {store_block}

  <div class="panel">
    <h3>Kontakt</h3>
    <p>Fragen, Fehler oder Wünsche: <a href="mailto:{EMAIL}">{EMAIL}</a><br>
    Bitte nennen Sie Gerät, Betriebssystem-Version und App-Version.
    Ich antworte in der Regel innerhalb von zwei Werktagen.</p>
  </div>

  <h2>Häufige Fragen</h2>
  {faq_html}

  <h2 id="datenschutz">Datenschutz</h2>
  <p>Stand: Juli 2026 · Verantwortlich: {DEV}, erreichbar unter
  <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <p><strong>Keine Datenerhebung durch den Entwickler.</strong> Die App
  erhebt, speichert und überträgt keine personenbezogenen Daten an mich oder an
  Dritte. Es sind keine Analyse-, Tracking- oder Werbedienste eingebunden, und
  es besteht kein Nutzerkonto.</p>
  {privacy_extra_html}
  <p><strong>Speicherung auf dem Gerät.</strong> Alle in der App erfassten
  Inhalte werden ausschließlich lokal gespeichert und sind nur auf Ihrem Gerät
  verfügbar. Sie können sie jederzeit in der App löschen; beim Entfernen der App
  werden sie ebenfalls gelöscht. Für Ihre eigene Datensicherung sind Sie
  verantwortlich – etwa über ein verschlüsseltes Geräte-Backup.</p>
  <p><strong>Käufe.</strong> Ein In-App-Kauf wird ausschließlich über Apple
  abgewickelt. Die Zahlungsdaten verarbeitet Apple; ich erhalte weder
  Zahlungsdaten noch Ihre Apple-ID. Für diesen Vorgang gilt Apples
  Datenschutzerklärung.</p>
  <p><strong>Ihre Rechte.</strong> Da mir keine personenbezogenen Daten
  vorliegen, kann ich keine Auskunft über gespeicherte Daten erteilen – es sind
  schlicht keine vorhanden. Wenn Sie mir eine E-Mail schreiben, verarbeite ich
  Ihre Adresse und Ihre Nachricht ausschließlich zur Beantwortung Ihrer Anfrage
  und lösche sie, sobald der Vorgang abgeschlossen ist.</p>

  <p><a href="../support/">← Zurück zur Support-Übersicht</a></p>
</div></div>
"""
    write(f"{slug}/index.html",
          head(f"{app['name']} – Support & Datenschutz",
               f"Support, häufige Fragen und Datenschutzhinweise zur App "
               f"{app['name']}.", 1)
          + body + foot(1))


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build_index()
    build_support_hub()
    for app in APPS:
        if app.get("slug"):
            build_app_page(app)


if __name__ == "__main__":
    main()
