# Beispiele für manubot-ai-editor

Dieses Verzeichnis enthält Beispiel-Konfigurationen und Skripte für die Verwendung von manubot-ai-editor.

## Dateien

### `dissertation_generator.py`

Ein vollständiges Python-Skript für die phasenweise Erstellung einer Dissertation mit dem optimierten Prompt-Design (APA 7, Deutsch).

**Verwendung:**

```bash
# OpenAI API Key setzen
export OPENAI_API_KEY=your_api_key_here

# Skript ausführen
python examples/dissertation_generator.py
```

Das Skript führt Sie interaktiv durch die folgenden Phasen:
1. **Outline** - Generierung des Inhaltsverzeichnisses
2. **Abstract** - Erstellung des Abstracts
3. **Kapitel** - Schrittweise Generierung aller Kapitel
4. **Literaturverzeichnis** - Erstellung des vollständigen Literaturverzeichnisses

Die generierten Dateien werden im Verzeichnis `dissertation_output/` gespeichert.

**Konfiguration:**

Das Skript verwendet die folgenden Umgebungsvariablen (optional):
- `AI_EDITOR_MODEL_PROVIDER`: Provider ("openai" oder "anthropic", Standard: "openai")
- `AI_EDITOR_LANGUAGE_MODEL`: Modellname (Standard: "gpt-4o-mini")
- `OPENAI_API_KEY`: API-Schlüssel für OpenAI
- `ANTHROPIC_API_KEY`: API-Schlüssel für Anthropic

### `dissertation-prompts.yaml`

Beispiel-Konfigurationsdatei für die Überarbeitung von Dissertation-Abschnitten mit manubot-ai-editor.

**Verwendung:**

1. Kopieren Sie diese Datei in das `ci/` Verzeichnis Ihres Manubot-Manuskripts
2. Benennen Sie sie in `ai-revision-prompts.yaml` um
3. Passen Sie die Prompts nach Bedarf an

Diese Datei enthält spezialisierte Prompts für:
- Abstract
- Einleitung
- Theoretischer Rahmen / Literaturreview
- Methodik
- Ergebnisse
- Diskussion
- Schluss
- Literaturverzeichnis

### `dissertation-config.yaml`

Beispiel-Konfigurationsdatei für die Zuordnung von Prompts zu Dateien.

**Verwendung:**

1. Kopieren Sie diese Datei in das `ci/` Verzeichnis Ihres Manubot-Manuskripts
2. Benennen Sie sie in `ai-revision-config.yaml` um
3. Passen Sie die Dateinamen-Muster (Regex) an Ihre tatsächlichen Dateinamen an

Die Datei verwendet reguläre Ausdrücke, um Dateien bestimmten Prompts zuzuordnen. Passen Sie die Muster an Ihre Dateinamen-Konventionen an.

## Weitere Informationen

Für detaillierte Informationen zum Best-Practice-Prompt-Design siehe:
- [Dissertation Prompt Design Dokumentation](../docs/dissertation-prompt-design.md)
- [Custom Prompts Dokumentation](../docs/custom-prompts.md)

