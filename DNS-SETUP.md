# harun.app auf diese Website umstellen

> **Status 2026-07-30: ZURÜCKGESTELLT.** Der Namecheap-Zugang für `harun.app`
> ist nicht auffindbar (Passwort-Reset kam nicht an, keine Namecheap-Mails im
> Postfach). Stattdessen wird in App Store Connect direkt auf
> `https://tayyare79.github.io/...` verwiesen — die URLs sind bereits in
> Entwurfs-Versionen hinterlegt und gehen mit dem jeweils nächsten App-Update
> live. Diese Anleitung bleibt für den Fall, dass der Domain-Zugang wieder
> auftaucht.
>
> **Achtung:** `harun.app` läuft am **10.02.2027** ab. Ohne Zugang wird sie
> nicht verlängert. Solange noch veröffentlichte App-Versionen auf `harun.app`
> zeigen (aktuell Leichenschau und GOÄ), sollten deren Updates vorher
> eingereicht werden.

Ziel: `https://harun.app` soll diese GitHub-Pages-Website ausliefern statt der
leeren React-Platzhalterseite auf dem Namecheap-Hosting.

Warum: In App Store Connect ist bei **Leichenschau Abrechnung** und
**GOÄ Abrechnung** `https://harun.app` als Support- und Datenschutz-URL
hinterlegt. Apple lässt diese Felder bei bereits veröffentlichten Versionen
nicht mehr ändern („To make changes to the app name, category, or privacy
policy, create a new app version"). Wenn stattdessen die Domain auf diese
Website zeigt, sind beide Apps sofort korrekt – ohne neue Version und ohne
Review.

## Schritt 1 – DNS bei Namecheap ändern

Namecheap → **Domain List** → bei `harun.app` auf **Manage** → Reiter
**Advanced DNS** → Abschnitt **Host Records**.

Den bestehenden A-Record `@ → 162.0.217.90` löschen und stattdessen diese
vier A-Records anlegen:

| Type     | Host | Value             | TTL       |
|----------|------|-------------------|-----------|
| A Record | @    | 185.199.108.153   | Automatic |
| A Record | @    | 185.199.109.153   | Automatic |
| A Record | @    | 185.199.110.153   | Automatic |
| A Record | @    | 185.199.111.153   | Automatic |

Zusätzlich für die www-Adresse:

| Type        | Host | Value                    | TTL       |
|-------------|------|--------------------------|-----------|
| CNAME Record| www  | tayyare79.github.io.     | Automatic |

**Nicht anfassen:** MX-Records und alles, was mit E-Mail zu tun hat – sonst
kommen keine Mails mehr an. Ebenso TXT-Records (SPF/DKIM) unverändert lassen.

Falls Namecheap einen `URL Redirect Record` oder `CNAME @` anzeigt: entfernen,
sonst kollidiert er mit den A-Records.

## Schritt 2 – Custom Domain in GitHub aktivieren

Erst **nachdem** die DNS-Änderung greift (Prüfung: `dig +short harun.app`
liefert `185.199.…`). Sonst leitet GitHub `tayyare79.github.io` auf eine
Domain um, die noch die alte Seite zeigt.

```bash
gh api -X PUT repos/tayyare79/tayyare79.github.io/pages -f cname=harun.app
echo "harun.app" > CNAME && git add CNAME && git commit -m "Custom domain" && git push
```

Danach in den Repo-Einstellungen **Enforce HTTPS** aktivieren (oder abwarten,
GitHub stellt das Zertifikat automatisch aus, sobald DNS stimmt).

## Schritt 3 – Kontrolle

```bash
curl -sI https://harun.app | head -1          # 200
curl -s https://harun.app | grep -o "<title>.*</title>"
```

Erwartet: `Harun Nakas – Apps für iPhone, iPad und Mac`

## Danach gilt

- `https://harun.app` → Landingpage (gültige Supportseite für Leichenschau und GOÄ)
- `https://harun.app/leichenschau/` → Support + Datenschutz Leichenschau
- `https://harun.app/goae/` → Support + Datenschutz GOÄ
- `https://tayyare79.github.io/...` leitet dauerhaft auf `harun.app/...` um,
  die bereits in App Store Connect gesetzten Pfade funktionieren also weiter.

## Optional später

Bei der jeweils nächsten regulären App-Version die Support-URL von
`https://harun.app` auf den genauen App-Pfad ändern
(z. B. `https://harun.app/leichenschau/`) und die Datenschutz-URL auf
`https://harun.app/leichenschau/#datenschutz`.
