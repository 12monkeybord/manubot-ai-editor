#!/usr/bin/env python3
"""
Beispiel-Skript für die phasenweise Erstellung einer Dissertation
mit dem optimierten Prompt-Design (APA 7, Deutsch).

Dieses Skript demonstriert, wie das Best-Practice-Prompt-Design
für die vollständige Erstellung einer Dissertation verwendet werden kann.

Verwendung:
    python examples/dissertation_generator.py

Voraussetzungen:
    - OpenAI API Key als Umgebungsvariable OPENAI_API_KEY gesetzt
    - Optional: Anthropic API Key als ANTHROPIC_API_KEY gesetzt
"""

import os
import json
import time
import textwrap
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("Bitte installieren Sie das openai-Paket: pip install openai")
    exit(1)

# System-Prompt für die Dissertation-Erstellung
SYSTEM_PROMPT = """<<<SYSTEM>>>
Du bist ein hochqualifizierter KI-gestützter wissenschaftlicher Schreibassistent (M.Sc./Ph.D.-Level) für die Fachrichtung Medizin / Medizinische Philosophie (z. B. Carl Gustav von Carus).  

Deine Aufgabe ist es, **einen vollständigen Dissertation-Entwurf** nach den Vorgaben des *APA-7-Stils* zu erzeugen. Der Text soll **flüssigen deutschen Fließtext** enthalten – keine Aufzählungen, keine Bullet-Points – und jede inhaltliche Aussage muss mit mindestens **einem echten PubMed-Artikel** belegt werden.  

Arbeite **phasenweise** und warte nach jeder Phase auf die Bestätigung des Nutzers, bevor du weitermachst. Verwende folgende Format- und Inhaltsvorgaben:

1. **Outline**  
   - Max. 500 Wörter  
   - Enthält ein **Inhaltsverzeichnis (ToC)** mit Haupt- und Unterkapiteln.  

2. **Abstract**  
   - Max. 250 Wörter, zusammenfassend Ziel, Methode, Ergebnisse, Schlussfolgerungen.  

3. **Kapitel** (jeweils max. 1.500 Wörter)  
   - **Einleitung** (Problemstellung, Forschungsfrage)  
   - **Theoretischer Rahmen / Literaturreview** (mind. 5 aktuelle PubMed-Quellen)  
   - **Methodik** (kurz, passend zum Fachgebiet)  
   - **Ergebnisse** (hypothetisch, logisch nachvollziehbar)  
   - **Diskussion** (Einordnung, Limitationen, Ausblick)  
   - **Schluss** (Kernergebnisse, Beitrag)  

4. **Literaturverzeichnis** (APA 7, alphabetisch, vollständige DOI-Angaben).  

**Zitierregeln:**  
- In-Text-Zitate: (Autor Jahr). Bei mehreren Autoren: (Autor et al., Jahr).  
- Jeder Satz, der faktische Information enthält, muss mindestens ein Zitat besitzen.  
- Verwende ausschließlich **reale PubMed-Artikel** (z. B. DOI 10.1000/xyz). Halluziniere keine Quellen.  

**Stil:**  
- Wissenschaftlich-formal, akademisch, sachlich.  
- Verwende Übergangssätze (z. B. „Im Folgenden …", „Daher …") für flüssige Lesbarkeit.  
- Keine Aufzählungs- oder Bullet-Points, ausschließlich Fließtext.  

**Workflow:**  
- **Phase 1:** Generiere die Outline (ToC) und liefere sie zwischen den Tags ```<OUTLINE>``` … ```</OUTLINE>```. Warte dann auf die Nutzer-Bestätigung.  
- **Phase 2-4:** Auf Anfrage des Nutzers (z. B. „Bitte erstelle das Abstract"), generiere den jeweiligen Abschnitt zwischen den entsprechenden Tags (```<ABSTRACT>``` … ```</ABSTRACT>```, ```<CHAPTER_1>``` … ```</CHAPTER_1>``` usw.).  
- **Phase 5:** Erstelle das vollständige Literaturverzeichnis zwischen ```<REFERENCES>``` … ```</REFERENCES>```.

**Hinweis für den Nutzer:**  
- Solltest du konkrete PubMed-DOIs besitzen, lege sie dem Prompt in einer separaten Liste (```<DOI_LIST>…</DOI_LIST>```) bei, damit sie präzise verwendet werden können.  
- Andernfalls generiere plausible Beispiele und markiere sie mit „*Platzhalter – bitte prüfen*".

Wenn du das verstanden hast, antworte bitte ausschließlich mit:  
```Ready```  

Warte anschließend auf die Nutzereingabe für das Thema.
<<<END>>>
"""


class DissertationGenerator:
    """Generator für phasenweise Dissertation-Erstellung."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        provider: str = "openai",
        temperature: float = 0.2,
        max_tokens: int = 3000,
    ):
        """
        Initialisiert den Dissertation-Generator.

        Args:
            api_key: API-Schlüssel für den LLM-Provider
            model: Modellname (z.B. "gpt-4o-mini", "gpt-4o", "gpt-4-turbo")
            provider: Provider ("openai" oder "anthropic")
            temperature: Temperatur für die Textgenerierung (0.0-1.0)
            max_tokens: Maximale Anzahl von Tokens pro Antwort
        """
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # API-Key aus Umgebungsvariable oder Parameter
        if api_key is None:
            if provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
            elif provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
            else:
                raise ValueError(f"Unbekannter Provider: {provider}")

        if api_key is None:
            raise ValueError(
                f"API-Key für {provider} nicht gefunden. "
                f"Bitte setzen Sie {provider.upper()}_API_KEY als Umgebungsvariable."
            )

        # Client initialisieren
        if provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "anthropic":
            try:
                from anthropic import Anthropic

                self.client = Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError(
                    "Bitte installieren Sie das anthropic-Paket: pip install anthropic"
                )
        else:
            raise ValueError(f"Unbekannter Provider: {provider}")

        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def chat(self, user_message: str) -> str:
        """
        Sendet eine Nachricht an das LLM und gibt die Antwort zurück.

        Args:
            user_message: Die Benutzernachricht

        Returns:
            Die Antwort des LLMs
        """
        self.messages.append({"role": "user", "content": user_message})

        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            content = response.choices[0].message.content
        elif self.provider == "anthropic":
            # Anthropic verwendet ein anderes Format
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=self.messages,
            )
            content = response.content[0].text

        self.messages.append({"role": "assistant", "content": content})
        return content

    def ask_user(self, text: str) -> str:
        """
        Fragt den Benutzer nach Eingabe.

        Args:
            text: Die Frage an den Benutzer

        Returns:
            Die Benutzereingabe
        """
        print("\n" + "=" * 80)
        print("BENUTZEREINGABE ERFORDERLICH")
        print("=" * 80)
        print(textwrap.fill(text, width=80))
        return input("\n> ")

    def extract_tagged_content(self, text: str, tag: str) -> Optional[str]:
        """
        Extrahiert Inhalt zwischen XML-ähnlichen Tags.

        Args:
            text: Der Text, aus dem extrahiert werden soll
            tag: Der Tag-Name (z.B. "OUTLINE", "ABSTRACT")

        Returns:
            Der extrahierte Inhalt oder None
        """
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"

        start_idx = text.find(start_tag)
        end_idx = text.find(end_tag)

        if start_idx == -1 or end_idx == -1:
            return None

        start_idx += len(start_tag)
        return text[start_idx:end_idx].strip()

    def generate_outline(self, thema: str, fachgebiet: str, ziel_wortzahl: str) -> str:
        """
        Generiert die Outline (Inhaltsverzeichnis) der Dissertation.

        Args:
            thema: Das Thema der Dissertation
            fachgebiet: Das Fachgebiet
            ziel_wortzahl: Die Ziel-Wortzahl

        Returns:
            Die generierte Outline
        """
        user_prompt = f"""Thema: **"{thema}"**  
Fachgebiet: **{fachgebiet}**  
Ziel-Wortzahl Gesamtdoktorarbeit: **{ziel_wortzahl}**  
Bitte zuerst die **Outline** (Inhaltsverzeichnis) erzeugen."""

        print("\n" + "=" * 80)
        print("GENERIERE OUTLINE...")
        print("=" * 80)

        response = self.chat(user_prompt)
        print(response)

        outline = self.extract_tagged_content(response, "OUTLINE")
        if outline:
            return outline
        return response

    def generate_abstract(self) -> str:
        """
        Generiert das Abstract der Dissertation.

        Returns:
            Das generierte Abstract
        """
        user_prompt = "Bitte erstelle das Abstract."

        print("\n" + "=" * 80)
        print("GENERIERE ABSTRACT...")
        print("=" * 80)

        response = self.chat(user_prompt)
        print(response)

        abstract = self.extract_tagged_content(response, "ABSTRACT")
        if abstract:
            return abstract
        return response

    def generate_chapter(self, chapter_name: str, chapter_number: int) -> str:
        """
        Generiert ein Kapitel der Dissertation.

        Args:
            chapter_name: Der Name des Kapitels (z.B. "Einleitung", "Methodik")
            chapter_number: Die Kapitelnummer

        Returns:
            Das generierte Kapitel
        """
        user_prompt = f"Bitte erstelle Kapitel {chapter_number}: {chapter_name}."

        print("\n" + "=" * 80)
        print(f"GENERIERE KAPITEL {chapter_number}: {chapter_name}...")
        print("=" * 80)

        response = self.chat(user_prompt)
        print(response)

        chapter_tag = f"CHAPTER_{chapter_number}"
        chapter = self.extract_tagged_content(response, chapter_tag)
        if chapter:
            return chapter
        return response

    def generate_references(self, doi_list: Optional[list[str]] = None) -> str:
        """
        Generiert das Literaturverzeichnis.

        Args:
            doi_list: Optionale Liste von DOIs, die verwendet werden sollen

        Returns:
            Das generierte Literaturverzeichnis
        """
        if doi_list:
            doi_text = "\n".join(f"- {doi}" for doi in doi_list)
            user_prompt = f"""Bitte erstelle das vollständige Literaturverzeichnis.

<DOI_LIST>
{doi_text}
</DOI_LIST>"""
        else:
            user_prompt = "Bitte erstelle das vollständige Literaturverzeichnis."

        print("\n" + "=" * 80)
        print("GENERIERE LITERATURVERZEICHNIS...")
        print("=" * 80)

        response = self.chat(user_prompt)
        print(response)

        references = self.extract_tagged_content(response, "REFERENCES")
        if references:
            return references
        return response

    def save_to_file(self, content: str, filename: str, output_dir: Path):
        """
        Speichert Inhalt in eine Datei.

        Args:
            content: Der zu speichernde Inhalt
            filename: Der Dateiname
            output_dir: Das Ausgabeverzeichnis
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
        filepath.write_text(content, encoding="utf-8")
        print(f"\n✓ Gespeichert: {filepath}")


def main():
    """Hauptfunktion für die interaktive Dissertation-Erstellung."""

    print("=" * 80)
    print("DISSERTATION-GENERATOR")
    print("Phasenweise Erstellung einer APA-7-konformen Dissertation (Deutsch)")
    print("=" * 80)

    # Konfiguration
    provider = os.getenv("AI_EDITOR_MODEL_PROVIDER", "openai")
    model = os.getenv("AI_EDITOR_LANGUAGE_MODEL", "gpt-4o-mini")

    try:
        generator = DissertationGenerator(provider=provider, model=model)
    except ValueError as e:
        print(f"Fehler: {e}")
        return

    # Phase 1: Outline
    thema = generator.ask_user("Bitte geben Sie das Thema Ihrer Dissertation ein:")
    fachgebiet = generator.ask_user("Bitte geben Sie das Fachgebiet ein:")
    ziel_wortzahl = generator.ask_user("Bitte geben Sie die Ziel-Wortzahl ein (z.B. ≈ 12.000 Wörter):")

    outline = generator.generate_outline(thema, fachgebiet, ziel_wortzahl)

    # Bestätigung für Outline
    confirm = generator.ask_user(
        "Outline prüfen → Eingabe 'OK' für Abstract, sonst neue Anweisungen:"
    )
    if confirm.strip().lower() != "ok":
        generator.chat(confirm)
        outline = generator.generate_outline(thema, fachgebiet, ziel_wortzahl)

    # Phase 2: Abstract
    abstract = generator.generate_abstract()

    # Phase 3: Kapitel
    chapters = []
    chapter_names = [
        "Einleitung",
        "Theoretischer Rahmen / Literaturreview",
        "Methodik",
        "Ergebnisse",
        "Diskussion",
        "Schluss",
    ]

    for i, chapter_name in enumerate(chapter_names, 1):
        chapter = generator.generate_chapter(chapter_name, i)
        chapters.append((chapter_name, chapter))

        if i < len(chapter_names):
            confirm = generator.ask_user(
                f"Kapitel {i} prüfen → Eingabe 'OK' für nächstes Kapitel, sonst neue Anweisungen:"
            )
            if confirm.strip().lower() != "ok":
                generator.chat(confirm)
                chapter = generator.generate_chapter(chapter_name, i)
                chapters[-1] = (chapter_name, chapter)

    # Phase 4: Literaturverzeichnis
    doi_list_input = generator.ask_user(
        "Optional: Bitte geben Sie eine komma-getrennte Liste von DOIs ein (oder Enter für automatische Generierung):"
    )
    doi_list = [doi.strip() for doi in doi_list_input.split(",")] if doi_list_input.strip() else None
    references = generator.generate_references(doi_list)

    # Speichern
    output_dir = Path("dissertation_output")
    generator.save_to_file(outline, "00_outline.md", output_dir)
    generator.save_to_file(abstract, "01_abstract.md", output_dir)

    for i, (chapter_name, chapter_content) in enumerate(chapters, 2):
        filename = f"{i:02d}_{chapter_name.lower().replace(' ', '_').replace('/', '_')}.md"
        generator.save_to_file(chapter_content, filename, output_dir)

    generator.save_to_file(references, "99_references.md", output_dir)

    print("\n" + "=" * 80)
    print("DISSERTATION ERFOLGREICH GENERIERT!")
    print(f"Alle Dateien wurden in '{output_dir}' gespeichert.")
    print("=" * 80)


if __name__ == "__main__":
    main()

