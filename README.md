# Wissensmagazin

Öffentliche, kostenlose GitHub-Pages-Website: https://felix13201.github.io/wissensmagazin/

## Formate
- **Magazin**: längere Wissensartikel und Reportagen (type: `magazin`)
- **KI-Briefing**: tagesaktuelle technische KI-Analysen (type: `ki-briefing`)

Beide Bereiche verwenden dieselbe Suche, Kapitel-Navigation, Dark Mode und Lesemodus.

## Veröffentlichung – manuell nach ChatGPT-Ausgabe
Die ChatGPT-Automationen schreiben nicht automatisch in das öffentliche GitHub-Repository. Nach Ausgabe des Artikels im jeweiligen Chat gilt:
- `Artikel veröffentlichen` fügt einen vollständigen Magazinartikel hinzu.
- `Briefing veröffentlichen` fügt das veröffentlichungsfertige KI-Tech-Briefing hinzu.

Dazu wird ein Objekt zu `articles.json` ergänzt. Pflichtfelder: `id`, `date` (YYYY-MM-DD), `title`, `subtitle`, `category`, `content`, `type`, `status` (`full`). Für KI-Briefings `type: "ki-briefing"`; für Magazintexte `type: "magazin"`.

**Keine gesonderte personalisierte Fassung:** Das ChatGPT-KI-Briefing wird bereits neutral für die öffentliche Veröffentlichung verfasst. Die Veröffentlichungsfreigabe erfolgt weiterhin manuell.

## Schutz vertraulicher Daten
Auf der öffentlich erreichbaren Website dürfen keine persönlichen Angaben zu ihrem Betreiber und keine nichtöffentlichen Informationen über Arbeitgeber, Kollegen, Kunden, interne Projekte, Tickets, IT-Systeme oder Netzwerkdaten stehen. Beispiele müssen allgemein, öffentlich belegt oder fiktiv sein. Vor jeder Veröffentlichung Namen, persönliche Bezüge, geschützte Informationen und Quellen verifizieren.

## Betrieb
Kein Login, keine bezahlte API, keine Datenbank. GitHub Pages veröffentlicht Dateien vom Main-Branch. Lesefortschritt und Präferenzen sind browserlokal gespeichert.