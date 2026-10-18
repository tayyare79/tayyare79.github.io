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
    dict(slug="deutschstart-kids", name="DeutschStart Kids", asc_id="6811046728",
         group="Alltag & Sonstiges", platforms="iPhone · iPad",
         tag="Kinder & Lernen",
         store_url="https://apps.apple.com/app/id6811046728",
         short="Offline Deutsch-Lern-App für Kinder von 4 bis 7 Jahren: "
               "Spiele und Aussprache, Elternbereich auf Deutsch, Türkisch "
               "und Englisch."),
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
    dict(slug="physikstart", name="PhysikStart", asc_id="",
         group="Alltag & Sonstiges", platforms="iPhone · iPad",
         tag="Bildung · bald verfügbar", unreleased=True,
         short="Physik für 4–14 Jahre: 72 Missionen in drei Lernstufen und sechs "
               "Experimentierwelten. Lernen auf Deutsch, Englisch und Türkisch – "
               "offline, ohne Werbung oder Tracking.",
         local_data=True),
]

APPS.append({'slug': 'chemiestart',
 'name': 'ChemieStart',
 'asc_id': '',
 'group': 'Alltag & Sonstiges',
 'platforms': 'iPhone · iPad',
 'tag': 'Bildung · bald verfügbar',
 'unreleased': True,
 'short': 'Chemie in 72 virtuellen Missionen entdecken. Drei Lernstufen, Deutsch, Englisch und '
          'Türkisch. Offline lernen, ohne Werbung und Tracking.',
 'local_data': True})
APP_CHEMIESTART_SUPPORT = {'intro': 'Support und Datenschutz für <strong>ChemieStart</strong>: 72 Missionen in sechs virtuellen '
          'Chemiewelten und drei frei wählbaren Lernstufen. Deutsch, Englisch und Türkisch. Für iPhone '
          'und iPad ab iOS/iPadOS 17. Die Veröffentlichung im App Store wird vorbereitet.',
 'stand': '18. Oktober 2026',
 'common_faq': [],
 'faq': [('Was ist kostenlos, was umfasst Plus?',
          '18 Missionen bleiben kostenlos. ChemieStart Plus schaltet alle 72 Missionen durch einen '
          'Einmalkauf frei. Deutschland: 9,99 €. In anderen Ländern gilt der im Elternbereich '
          'angezeigte App-Store-Preis. Kein Abo.'),
         ('Wie stelle ich Plus wieder her?',
          'Im Elternbereich mit Ihrer PIN anmelden und „Käufe wiederherstellen“ wählen. Verwenden Sie '
          'denselben Apple Account wie beim Kauf. Apple verwaltet den Kauf; das Zurücksetzen des '
          'Lernfortschritts löscht ihn nicht. Lernstände werden dabei nicht auf andere Geräte '
          'übertragen.'),
         ('Braucht die App Internet?',
          'Die Lerninhalte und alle enthaltenen OpenAI-Sprachaufnahmen funktionieren offline. Für Kauf '
          'und Wiederherstellung ist eine Verbindung zu Apple erforderlich. Es gibt kein App-Konto, '
          'keine Werbung, keine Analyse und kein Tracking.'),
         ('Welche Experimente sind sicher?',
          'Die App zeigt vereinfachte Modelle. Hitze, Feuer, Destillation und Gefahrstoffe bleiben '
          'ausschließlich virtuell. Optionale Küchenkarten sind standardmäßig ausgeschaltet, nur für '
          'Erwachsene zugänglich und enthalten Sicherheitshinweise. Keine gefährlichen Stoffe '
          'nachmischen.'),
         ('Was passiert mit der Eltern-PIN?',
          'Die PIN wird nur als gesalzener Hash im Schlüsselbund dieses Geräts gespeichert. Der '
          'Entwickler kann sie nicht lesen. Ein Schlüsselbundeintrag kann auch nach Löschen und '
          'Neuinstallation der App erhalten bleiben.'),
         ('English: purchase and privacy',
          '18 missions are free. ChemieStart Plus unlocks all 72 missions with one purchase, no '
          'subscription. The local App Store price appears in the parent area. Restore with the same '
          'Apple Account. Learning content and bundled AI-generated OpenAI narration work offline. '
          'Profiles, progress and notebook entries stay on the device; no ads, analytics, tracking or '
          'app account. Apple handles payment and purchase records. The developer receives no card '
          'details. Contact support by email; your address and message are used to handle the request.'),
         ('Türkçe: satın alma ve gizlilik',
          '18 görev ücretsizdir. ChemieStart Plus tek seferlik satın almayla 72 görevin tamamını açar; '
          'abonelik yoktur. Yerel App Store fiyatı ebeveyn alanında gösterilir. Geri yüklemek için aynı '
          'Apple Hesabını kullanın. Dersler ve uygulamadaki yapay zekâ ile üretilmiş OpenAI sesleri '
          'çevrimdışı çalışır. Profiller, ilerleme ve laboratuvar defteri cihazda kalır. Reklam, '
          'analiz, takip veya uygulama hesabı yoktur. Ödemeyi ve satın alma kayıtlarını Apple işler; '
          'geliştirici kart bilgilerini almaz. Destek e-postanız ve adresiniz yalnızca talebinizi '
          'yanıtlamak için işlenir.')],
 'privacy_html': '<p><strong>App-Daten bleiben auf dem Gerät.</strong> ChemieStart überträgt keine '
                 'Profilnamen, Lernfortschritte, Laborbucheinträge oder Sprachdaten an den Entwickler. '
                 'Es gibt kein Benutzerkonto, keine Werbung, kein Tracking, keine Analyse und keine '
                 'Drittanbieter-SDKs. Kamera, Mikrofon, Kontakte und Standort werden nicht '
                 'verwendet.</p><p><strong>Lokale Speicherung.</strong> Bis zu drei Profile, '
                 'Fortschritt, laufende Missionen, Laborbuch und Einstellungen werden lokal '
                 'gespeichert. Der Kaufstatus wird lokal zwischengespeichert. Die Eltern-PIN liegt '
                 'ausschließlich als gesalzener Hash im gerätegebundenen Schlüsselbund. Fortschritt und '
                 'Laborbuch lassen sich im Elternbereich zurücksetzen. Das Löschen der App entfernt '
                 'ihre App-Daten; der Schlüsselbundeintrag kann erhalten bleiben. Geräte-Backups werden '
                 'durch Ihre Apple-Einstellungen verwaltet.</p><p><strong>Vorlesestimme.</strong> Die '
                 'Sprachaufnahmen wurden vorab mit OpenAI erzeugt und sind im App-Paket enthalten. Beim '
                 'Vorlesen sendet die App weder Texte noch Stimmen an OpenAI. Es gibt keine '
                 'Mikrofonaufnahme und keine Sprachverarbeitung in der Cloud.</p><p><strong>Kauf und '
                 'Wiederherstellung.</strong> Apple StoreKit wickelt den optionalen Einmalkauf ab. '
                 'Apple verarbeitet Zahlung und Kaufhistorie; die App prüft die Kaufberechtigung. Der '
                 'Entwickler erhält keine Zahlungs- oder Kartendaten. Kauf und Wiederherstellung liegen '
                 'im geschützten Elternbereich.</p><p><strong>Support und Kontakt.</strong> '
                 'Verantwortlich ist Harun Nakas, erreichbar über die oben genannte Supportadresse. '
                 'Wenn Sie per E-Mail Kontakt aufnehmen, werden Ihre Adresse und Nachricht zur '
                 'Bearbeitung Ihrer Anfrage verwendet. Bitte senden Sie keine vertraulichen Daten aus '
                 'dem Laborbuch. Für die Website gelten die technischen Verarbeitungen des '
                 'Hosting-Anbieters GitHub Pages.</p>'}

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
    "deutschstart-kids": dict(
        intro="Support und Datenschutz für die App <strong>DeutschStart Kids</strong> – "
              "die Offline-App zum Deutschlernen für Kinder von 4 bis 7 Jahren "
              "(Kindergarten bis Schulstart). Spielerische Übungen mit Aussprache "
              "und ein Elternbereich auf Deutsch, Türkisch und Englisch.",
        faq=[
            ("Funktioniert die App ohne Internet?",
             "Ja, vollständig. Alle Inhalte, Spiele und die Aussprache sind in der "
             "App enthalten – es wird keine Internetverbindung benötigt."),
            ("Wie bekomme ich eine bessere (Premium-)Stimme für die Aussprache?",
             "Die App nutzt die deutschen Stimmen Ihres Geräts. Eine hochwertigere "
             "Stimme laden Sie so: iOS-Einstellungen → Bedienungshilfen → "
             "Gesprochene Inhalte → Stimmen → Deutsch – dort eine Premium-Stimme "
             "auswählen und laden. Die App verwendet sie danach automatisch."),
            ("Wie funktioniert das Abo?",
             "Das Abo wird ausschließlich über Apple abgeschlossen und abgerechnet. "
             "Verwalten oder kündigen können Sie es jederzeit in den Einstellungen "
             "Ihrer Apple-ID unter „Abonnements“ – nicht in der App selbst."),
            ("Wo wird der Lernfortschritt gespeichert?",
             "Nur lokal auf Ihrem Gerät. Der Fortschritt wird nicht an den "
             "Entwickler oder an Dritte übertragen. Beim Löschen der App wird er "
             "ebenfalls entfernt."),
            ("Was ist das Parent-Gate (Elternsicherung)?",
             "Der Elternbereich – etwa für Einstellungen und Käufe – ist durch eine "
             "kleine Aufgabe geschützt, die nur Erwachsene lösen können. So können "
             "Kinder diese Bereiche nicht versehentlich öffnen."),
        ],
        stand="September 2026",
        privacy_extra="Lernfortschritt und Einstellungen werden ausschließlich "
                      "lokal auf Ihrem Gerät gespeichert (UserDefaults) und "
                      "nicht an Server übertragen.",
        purchase_html="<p><strong>Käufe.</strong> In-App-Käufe und Abos werden "
                      "ausschließlich über Apple abgewickelt. Die Zahlungsdaten "
                      "verarbeitet Apple; ich erhalte weder Zahlungsdaten noch "
                      "Ihre Apple-ID. Für diesen Vorgang gilt Apples "
                      "Datenschutzerklärung.</p>",
    ),
    "mathestart": dict(
        intro="Support und Datenschutz für <strong>MatheStart</strong> – Mathematik für Kinder von etwa 4 bis 7 Jahren.",
        faq=[
            ("Für welches Alter ist die App?", "Für Kinder von etwa 4 bis 7 Jahren. Der Elternbereich ist durch eine Rechenaufgabe geschützt."),
            ("Braucht die App Internet?", "Die Lerninhalte, Bilder, Sprachaufnahmen und Fortschritte funktionieren offline. Für den optionalen Kauf und die Wiederherstellung ab Version 1.2 ist eine Verbindung zum App Store erforderlich."),
            ("Gibt es ein Abo oder In-App-Käufe?", "Kein Abo. Ab Version 1.2 schaltet das optionale Paket „Rechnen bis 20“ durch einen Einmalkauf 20 Zusatzlektionen dauerhaft frei. Spätere eigenständige Pakete sind nicht enthalten. Vier Einstiegslektionen und alle fünf bisherigen Spielwelten bleiben kostenlos. Der Preis steht im geschützten Elternbereich in Ihrer Landeswährung. Version 1.1 und ältere Versionen enthalten diesen Kauf noch nicht."),
            ("Wie stelle ich den Kauf wieder her?", "Im Elternbereich auf „Käufe wiederherstellen“ tippen und denselben Apple Account verwenden. Das Zurücksetzen des Lernfortschritts entfernt den Kauf nicht."),
            ("English: purchases and privacy", "From version 1.2, the optional Maths up to 20 pack permanently unlocks 20 extra lessons with a one-time purchase. No subscription; future separate packs are not included. Four introductory lessons and all five existing worlds remain free. Learning content works offline. Purchase and restore require Apple connectivity and are parent-gated. Apple processes payment and purchase records; the developer receives no payment-card details. Learning progress stays on the device. No ads, analytics, tracking or child accounts."),
            ("Türkçe: satın alma ve gizlilik", "1.2 sürümünden itibaren isteğe bağlı 20’ye kadar matematik paketi, tek seferlik satın almayla 20 ek dersi kalıcı olarak açar. Abonelik yoktur; gelecekteki ayrı paketler dahil değildir. İlk dört ders ve mevcut beş oyun dünyası ücretsiz kalır. Dersler çevrimdışı çalışır. Satın alma ve geri yükleme Apple bağlantısı gerektirir ve ebeveyn kilidi arkasındadır. Ödeme ve satın alma kayıtlarını Apple işler; geliştirici kart bilgilerini almaz. Öğrenme ilerlemesi cihazda kalır. Reklam, analiz, takip veya çocuk hesabı yoktur."),
        ],
        privacy_extra="Stand für MatheStart: 27. September 2026. Bilder und Sprachaufnahmen sind in der App enthalten; Apple-Sprachausgabe auf dem Gerät dient als Ersatz. Kein Cloud-TTS und keine Übertragung von Kinderstimmen oder Lernständen. Ab Version 1.2 ist ein optionaler Einmalkauf über Apple StoreKit verfügbar. Apple verarbeitet Zahlung und Kaufhistorie; die App prüft die Kaufberechtigung auf dem Gerät. Wir erhalten keine Zahlungs- oder Kartendaten. Kauf, Wiederherstellung und externe Links sind durch die Elternsperre geschützt. Lernfortschritt und Einstellungen bleiben lokal und können im Elternbereich zurückgesetzt werden. Der Kauf bleibt dabei erhalten.",
    ),
    "physikstart": dict(
        intro="Support und Datenschutz für <strong>PhysikStart</strong>: Physik entdecken "
              "für Kinder und Jugendliche von etwa 4 bis 14 Jahren, mit drei Lernstufen, "
              "sechs Experimentierwelten und 72 Missionen auf Deutsch, Englisch und Türkisch. "
              "Für iPhone und iPad ab iOS/iPadOS 17. Die Experimente verwenden vereinfachte Modelle.",
        stand="18. Oktober 2026",
        release_notice="<p>Die Veröffentlichung im App Store wird vorbereitet.</p>",
        common_faq=[],
        faq=[
            ("Was ist kostenlos, was umfasst PhysikStart Plus?",
             "18 vollständige Missionen, die Schattenwerkstatt, alle drei Sprachen und bis zu "
             "drei lokale Profile bleiben kostenlos. PhysikStart Plus schaltet durch einen "
             "einmaligen Kauf 54 weitere Missionen (insgesamt 72) und alle sechs offenen Labore frei. "
             "Kein Abonnement. Der Preis wird im geschützten Elternbereich in Ihrer Landeswährung "
             "angezeigt. Spätere eigenständige Pakete sind nicht zugesagt."),
            ("Braucht die App Internet?",
             "Lerninhalte, Experimente, Forscherbuch und die enthaltenen Sprachaufnahmen funktionieren "
             "offline. Kauf, Wiederherstellung und die Prüfung des Kaufstatus über Apple können eine "
             "App-Store-Verbindung benötigen. Es gibt kein App-Konto und keinen eigenen Server für Lerndaten."),
            ("Wie stelle ich einen Kauf wieder her?",
             "Öffnen Sie den Elternbereich mit Ihrer PIN und tippen Sie auf „Käufe wiederherstellen“. "
             "Verwenden Sie denselben Apple Account wie beim Kauf. Das Zurücksetzen des Lernfortschritts "
             "löscht den Kauf nicht. Kauf und Wiederherstellung übertragen kein Forscherbuch auf ein anderes Gerät."),
            ("Wie funktionieren Profile, Forscherbuch und Löschen?",
             "Bis zu drei Profile speichern Namen oder Spitznamen, Lernstufe, Fortschritt und Versuche "
             "lokal. Im Elternbereich können Sie Namen ändern, den Fortschritt des gewählten Profils "
             "zurücksetzen und zusätzliche Profile löschen; ein Profil bleibt bestehen. Es gibt keine "
             "Synchronisierung zwischen Geräten durch die App. Betriebssystem-Backups richten sich "
             "nach Ihren Geräteeinstellungen."),
            ("Was schützt die Eltern-PIN, und was passiert bei einer vergessenen PIN?",
             "Eine sechsstellige PIN schützt Käufe, Profile und Einstellungen. Erwachsene sollten sie "
             "selbst einrichten; die Einrichtung prüft weder Alter noch Elternrolle. Die PIN lässt sich "
             "mit der bisherigen PIN ändern. Es gibt keinen Wiederherstellungs- oder Umgehungscode. "
             "Bitte löschen Sie die App nicht als Entsperrversuch: Lerndaten können verloren gehen, "
             "während der PIN-Prüfwert im Schlüsselbund erhalten bleibt."),
            ("Woher kommen die Stimmen? Wird mein Kind aufgenommen?",
             "Die enthaltenen Sprachaufnahmen wurden vorab mit KI-Spracherzeugung erstellt und werden "
             "lokal abgespielt. Es wird kein KI-Dienst während der Nutzung aufgerufen. Wenn eine Aufnahme "
             "nicht verfügbar ist, kann eine vorhandene Systemstimme auf dem Gerät einspringen. Ohne "
             "passende Stimme bleiben alle Texte lesbar. Vorlesen und Versuchstöne starten nur nach "
             "Antippen; verwenden Sie eine niedrige Gerätelautstärke. Die App nutzt kein Mikrofon und "
             "zeichnet keine Kinderstimmen auf."),
            ("Wie melde ich ein Problem?",
             f"Schreiben Sie an <a href=\"mailto:{EMAIL}\">{EMAIL}</a> und nennen Sie Gerät, "
             "iOS-/iPadOS-Version, App-Version und die betroffene Mission. Bitte senden Sie keine "
             "Eltern-PIN, Namen von Kindern oder ungeschwärzten persönlichen Screenshots."),
            ("English: support and purchases",
             "PhysikStart offers physics activities for ages 4–14 in German, English and Turkish. "
             "18 missions, the shadow lab, all languages and up to three local profiles are free. "
             "A one-time PhysikStart Plus purchase unlocks 54 more missions and all six open labs; "
             "there is no subscription or promise of future separate packs. Learning works offline. "
             "Purchases, restore and Apple entitlement checks may need internet. Restore in the PIN-protected "
             "parent area using the same Apple Account. Learning progress does not sync through the app. "
             "A forgotten PIN cannot be reset or bypassed; deleting the app may lose progress without "
             "removing its Keychain PIN record. Contact the email above with device, OS, app version and "
             "mission, without children's names or your PIN. Privacy details in English follow below."),
            ("Türkçe: destek ve satın alma",
             "PhysikStart, 4–14 yaş için Almanca, İngilizce ve Türkçe fizik etkinlikleri sunar. "
             "18 görev, gölge laboratuvarı, tüm diller ve en fazla üç yerel profil ücretsizdir. "
             "Tek seferlik PhysikStart Plus satın alımı 54 ek görevi ve altı serbest laboratuvarın tümünü açar. "
             "Abonelik yoktur; gelecekteki ayrı paketler vaat edilmez. Öğrenme çevrimdışı çalışır. "
             "Satın alma, geri yükleme ve Apple satın alma hakkı kontrolleri internet gerektirebilir. "
             "PIN korumalı ebeveyn alanında aynı Apple Hesabı ile satın alımları geri yükleyebilirsiniz. "
             "Uygulama öğrenme ilerlemesini cihazlar arasında eşitlemez. Unutulan PIN için kurtarma veya "
             "atlama kodu yoktur; uygulamayı silmek ilerlemeyi kaybettirebilir, ancak Anahtar Zinciri PIN "
             "kaydı kalabilir. Destek için yukarıdaki adrese cihaz, sistem ve uygulama sürümü ile görevi "
             "yazın; çocuk adı veya PIN göndermeyin. Türkçe gizlilik bilgileri aşağıdadır."),
        ],
        privacy_html="""<p><strong>Lokale Lern-App.</strong> PhysikStart hat keine Nutzerkonten, Werbung,
  Analyse- oder Trackingdienste. Profile mit Namen oder Spitznamen, Lernstufe, Einstellungen,
  Missionsentwürfe und Forscherbuch werden auf dem Gerät gespeichert. Die App überträgt diese
  Kinder- und Lerndaten nicht an den Entwickler oder an KI-Dienste. Sie benötigt weder Mikrofon
  noch Kamera, Kontakte oder Standort.</p>
  <p><strong>Eltern-PIN und Backups.</strong> Ein gesalzener Prüfwert der PIN und Angaben zur
  Begrenzung von Fehlversuchen liegen im lokalen Apple-Schlüsselbund; die PIN wird nicht im Klartext
  gespeichert. Dieser Schlüsselbundeintrag wird von der App nicht über iCloud synchronisiert.
  Lernfortschritt lässt sich im Elternbereich zurücksetzen, zusätzliche Profile lassen sich löschen.
  Der PIN-Eintrag kann nach dem Entfernen der App bestehen bleiben. Ob das Betriebssystem andere
  App-Daten sichert oder wiederherstellt, hängt von Geräteeinstellungen und Apple-Diensten ab;
  die App bietet keine eigene Cloud-Sicherung oder geräteübergreifende Synchronisierung.</p>
  <p><strong>Vorlesen und KI.</strong> Vorproduzierte KI-Sprachaufnahmen gehören zum App-Paket.
  Ihre Wiedergabe erfolgt offline und nur auf Wunsch. Als Ersatz kann eine auf dem Gerät vorhandene
  Apple-Systemstimme genutzt werden. Es gibt keine Cloud-KI oder Cloud-Spracherzeugung während der
  App-Nutzung, keine Sprachaufnahme und keine Übermittlung von Kinderstimmen.</p>
  <p><strong>Apple-Käufe.</strong> Der optionale Einmalkauf PhysikStart Plus, Wiederherstellung
  und Kaufberechtigungen werden über Apple StoreKit abgewickelt. Apple verarbeitet die dafür
  erforderlichen Account-, Zahlungs- und Transaktionsdaten. Die App prüft die Kaufberechtigung;
  der Entwickler erhält keine Kartendaten. Es gilt ergänzend
  <a href="https://www.apple.com/legal/privacy/">Apples Datenschutzerklärung</a>.
  Die App sendet dabei keine Profile oder Lernstände an Apple.</p>
  <p><strong>Support und Datenschutzanfragen.</strong> Wenn Sie uns eine E-Mail schreiben,
  verarbeiten wir die Absenderadresse und Ihre Nachricht zur Bearbeitung der Anfrage.
  Diese Angaben werden gelöscht, sobald sie nicht mehr benötigt werden und keine gesetzlichen
  Aufbewahrungspflichten entgegenstehen. Bitte senden Sie keine PIN oder Daten von Kindern.
  Für Auskunft, Berichtigung oder Löschung von an uns gesendeten Angaben sowie andere
  Datenschutzfragen nutzen Sie die oben genannte Kontaktadresse. Sie können sich auch an eine
  Datenschutz-Aufsichtsbehörde wenden. Die lokal gespeicherten Lernprofile kann der Entwickler
  nicht auslesen oder aus der Ferne löschen.</p>
  <p><strong>Diese Support-Website.</strong> Die Seite wird über GitHub Pages bereitgestellt.
  Beim Aufruf verarbeitet der Hostinganbieter technische Zugriffsdaten, etwa die IP-Adresse;
  dies ist vom Offline-Betrieb der App getrennt. Auf dieser Seite sind keine Analyse- oder
  Werbeskripte eingebunden. Weitere Angaben stehen in der
  <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub-Datenschutzerklärung</a>.</p>
  <h3 lang="en">Privacy — English</h3>
  <p lang="en">The developer is Harun Nakas, reachable at the email above. Profiles (names or
  nicknames), learning progress, drafts and settings stay in local app storage; the app sends none
  of these to the developer or AI services. There are no accounts, ads, analytics, tracking, microphone
  recordings or live cloud AI. Preproduced AI narration is included and plays offline on request,
  with an available on-device Apple voice as fallback. A salted PIN verifier and failed-attempt
  limits are stored in the device Keychain without app-enabled iCloud synchronization; the record
  may survive app deletion. Progress can be reset and additional profiles deleted in the parent area.
  Operating-system backup and restore depend on device settings; the app provides no cloud sync.
  Apple handles payment, account and transaction data for the optional one-time purchase, restore
  and entitlement checks; the developer receives no card details. Profiles and progress are not sent
  to Apple by the app. If you email support, your address and message are processed to answer you
  and retained only as needed, subject to legal retention duties. Contact us for access, correction,
  deletion or other privacy requests; you may also contact a data protection authority. We cannot
  remotely read or erase local profiles. This GitHub Pages website may produce technical hosting
  logs, including IP addresses, separately from the offline app; it embeds no advertising or analytics
  scripts. Apple and GitHub privacy policies are linked above.</p>
  <h3 lang="tr">Gizlilik — Türkçe</h3>
  <p lang="tr">Veri sorumlusu, yukarıdaki e-posta adresinden ulaşabileceğiniz Harun Nakas’tır.
  Profil adları veya takma adlar, öğrenme ilerlemesi, taslaklar ve ayarlar cihazda saklanır;
  uygulama bunları geliştiriciye veya yapay zekâ hizmetlerine göndermez. Hesap, reklam, analiz,
  takip, mikrofon kaydı veya kullanım sırasında bulut yapay zekâsı yoktur. Önceden üretilmiş yapay
  zekâ sesleri uygulamaya dahildir ve istek üzerine çevrimdışı çalınır; gerekirse cihazda bulunan
  bir Apple sesi kullanılır. PIN’in kendisi yerine tuzlanmış doğrulama değeri ve hatalı deneme
  sınırları, uygulamanın iCloud eşitlemesini açmadığı cihaz Anahtar Zinciri’nde saklanır; bu kayıt
  uygulama silindikten sonra kalabilir. Ebeveyn alanında ilerleme sıfırlanabilir ve ek profiller
  silinebilir. İşletim sistemi yedekleme ve geri yüklemesi cihaz ayarlarına bağlıdır; uygulama bulut
  eşitlemesi sunmaz. İsteğe bağlı tek seferlik satın alma, geri yükleme ve hak kontrolleri için
  hesap, ödeme ve işlem verilerini Apple işler; geliştirici kart bilgilerini almaz. Uygulama profil
  veya ilerlemeyi Apple’a göndermez. Destek e-postanızdaki adres ve mesaj yanıt vermek için işlenir;
  gerekli süre ve yasal saklama yükümlülükleri dışında tutulmaz. Erişim, düzeltme, silme ve diğer
  gizlilik talepleri için bize, ayrıca yetkili veri koruma makamına başvurabilirsiniz. Yerel
  profilleri uzaktan okuyamaz veya silemeyiz. Bu GitHub Pages sitesinin barındırılması, çevrimdışı
  uygulamadan ayrı olarak IP adresi gibi teknik erişim kayıtları oluşturabilir; sayfada reklam veya
  analiz betikleri yoktur. Apple ve GitHub gizlilik açıklamaları yukarıda bağlantılıdır.</p>""",
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


def app_store_url(app):
    """Store-Link einer App – Standard-URL oder per `store_url` überschrieben."""
    return app.get("store_url") or store_url(app["asc_id"])


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
                f'<a href="{app_store_url(a)}">Im App Store</a>'
            cards.append(f"""  <article class="card">
    <span class="badge">{html.escape(a['tag'])}</span>
    <h3>{html.escape(a['name'])}</h3>
    <p>{a['short']}</p>
    <div class="links">
{('      ' + store) if store else ''}
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


APP_SUPPORT['chemiestart'] = APP_CHEMIESTART_SUPPORT


def build_app_page(app):
    slug = app["slug"]
    cfg = APP_SUPPORT[slug]
    faq = cfg["faq"] + cfg.get("common_faq", FAQ_COMMON)

    faq_html = "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq
    )

    store_block = cfg.get("release_notice", "")
    if not app.get("unreleased"):
        store_block = (f'<p><a class="btn" href="{app_store_url(app)}">'
                       f'Im App Store ansehen</a></p>')

    privacy_extra = cfg.get("privacy_extra", "")
    privacy_extra_html = f"<p>{privacy_extra}</p>" if privacy_extra else ""

    stand = cfg.get("stand", "Juli 2026")
    purchase_html = cfg.get("purchase_html",
        "<p><strong>Käufe.</strong> Ein In-App-Kauf wird ausschließlich über Apple\n"
        "  abgewickelt. Die Zahlungsdaten verarbeitet Apple; ich erhalte weder\n"
        "  Zahlungsdaten noch Ihre Apple-ID. Für diesen Vorgang gilt Apples\n"
        "  Datenschutzerklärung.</p>")

    privacy_html = cfg.get("privacy_html", f"""<p><strong>Keine Datenerhebung durch den Entwickler.</strong> Die App
  erhebt, speichert und überträgt keine personenbezogenen Daten an mich oder an
  Dritte. Es sind keine Analyse-, Tracking- oder Werbedienste eingebunden, und
  es besteht kein Nutzerkonto.</p>
  {privacy_extra_html}
  <p><strong>Speicherung auf dem Gerät.</strong> Alle in der App erfassten
  Inhalte werden ausschließlich lokal gespeichert und sind nur auf Ihrem Gerät
  verfügbar. Sie können sie jederzeit in der App löschen; beim Entfernen der App
  werden sie ebenfalls gelöscht. Für Ihre eigene Datensicherung sind Sie
  verantwortlich – etwa über ein verschlüsseltes Geräte-Backup.</p>
  {purchase_html}
  <p><strong>Ihre Rechte.</strong> Da mir keine personenbezogenen Daten
  vorliegen, kann ich keine Auskunft über gespeicherte Daten erteilen – es sind
  schlicht keine vorhanden. Wenn Sie mir eine E-Mail schreiben, verarbeite ich
  Ihre Adresse und Ihre Nachricht ausschließlich zur Beantwortung Ihrer Anfrage
  und lösche sie, sobald der Vorgang abgeschlossen ist.</p>""")

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
  <p>Stand: {stand} · Verantwortlich: {DEV}, erreichbar unter
  <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  {privacy_html}

  <p><a href="../support/">← Zurück zur Support-Übersicht</a></p>
</div></div>
"""
    if slug == "mathestart":
        body = body.replace("erhebt, speichert und überträgt keine personenbezogenen Daten an mich oder an\n  Dritte.", "überträgt keine Kinder- oder Lerndaten an den Entwickler. Die optionale\n  Kaufabwicklung erfolgt über Apple, wie unten beschrieben.")
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
