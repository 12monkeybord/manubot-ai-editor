# Prompt-Optimierung – Best Practice für ein automatisiertes, vollständig zitierfähiges Dissertation-Gerüst (APA 7 – Deutsch)

Diese Dokumentation beschreibt ein optimiertes Prompt-Design für die Erstellung einer vollständigen, APA-7-konformen Dissertation in deutscher Sprache. Dieses Design kann sowohl als eigenständiges System als auch in Kombination mit dem manubot-ai-editor verwendet werden.

## 1. Warum dieses Prompt-Design optimal ist

| Prinzip | Umsetzung im Prompt |
|--------|---------------------|
| **Klare Rollen-Definition** | Der *System-Prompt* setzt dich als „hochqualifizierten KI-gestützten Wissenschafts-Schreibassistenten" mit Fokus auf medizinisch-humanistische Fachgebiete. |
| **Explizite Ziel- und Format-Angaben** | Inklusion von *Abstract*, *Inhaltsverzeichnis (ToC)*, *Kapitel-Struktur*, *Durchgehender Fließtext* und *APA-7-Zitierstil* (In-Text- und Literaturverzeichnis). |
| **Schritt-für-Schritt-Workflow** | Das Prompt ist in **Phasen** unterteilt (Outline → Abstract → Kapitel → Literaturverzeichnis). So bleibt die Token-Auslastung im Rahmen und jede Phase kann separat geprüft werden. |
| **Verwendung von Delimitern** | Jeder Abschnitt des Dialogs (System, User, Output) ist eindeutig zwischen ```<<<SYSTEM>>>``` … ```<<<END>>>``` abgegrenzt – das verhindert „Prompt-Leakage" und erleichtert das Einbinden in API-Calls. |
| **Vorgaben zu Zitaten & Quellen** | Anweisung, **nur reale PubMed-Artikel** (oder bereits gelieferte DOI-Liste) zu benutzen, und jede Aussage mit **mindestens einem Zitat** zu belegen. |
| **Kontroll-Mechanismus** | Nach jeder Phase fordert das Prompt die Bestätigung des Nutzers („Bitte bestätige/ergänze das Outline …"), bevor mit dem nächsten Schritt fortgefahren wird. |
| **Wort-/Zeichen-Limitierung** | Für jede Phase ein klares Max-Länge-Kriterium (z. B. Abstract ≤ 250 Wörter, Kapitel ≤ 1.500 Wörter), um Überschreitungen zu vermeiden. |
| **Platzhalter für Nutzer-Eingaben** | `{THEMA}`, `{FACHGEBIET}`, `{FRAUENSTELLE}` usw. können vom Nutzer individuell ersetzt werden. |

## 2. Das komplette Prompt-Template (Deutsch)

```text
<<<SYSTEM>>>
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
```

## 3. Integration mit manubot-ai-editor

Das manubot-ai-editor System ist primär für die **Überarbeitung** bestehender Manuskripte ausgelegt und arbeitet paragraph-weise. Für die **Erstellung** einer vollständigen Dissertation mit dem oben beschriebenen phasenweisen Ansatz gibt es zwei Möglichkeiten:

### Option A: Verwendung für die Überarbeitung einzelner Abschnitte

Nachdem Sie eine Dissertation mit dem phasenweisen Prompt-Design erstellt haben, können Sie einzelne Abschnitte mit manubot-ai-editor überarbeiten. Hier ist eine Beispiel-Konfiguration:

**`ci/ai-revision-prompts.yaml`:**

```yaml
prompts:
  dissertation_abstract: |
    Du bist ein hochqualifizierter KI-gestützter wissenschaftlicher Schreibassistent.
    Überarbeite den folgenden Absatz aus dem Abstract einer Dissertation im APA-7-Stil.
    Stelle sicher, dass:
    - Der Text wissenschaftlich-formal und akademisch ist
    - Alle Zitate im Format (Autor Jahr) korrekt sind
    - Der Text flüssigen deutschen Fließtext darstellt (keine Aufzählungen)
    - Die maximale Länge von 250 Wörtern eingehalten wird
    
    Absatz: {paragraph_text}
    
    Überarbeiteter Absatz:

  dissertation_einleitung: |
    Du bist ein hochqualifizierter KI-gestützter wissenschaftlicher Schreibassistent.
    Überarbeite den folgenden Absatz aus der Einleitung einer Dissertation im APA-7-Stil.
    Stelle sicher, dass:
    - Die Problemstellung und Forschungsfrage klar dargestellt sind
    - Alle Zitate im Format (Autor Jahr) korrekt sind
    - Der Text wissenschaftlich-formal und akademisch ist
    - Jede faktische Aussage mit mindestens einem Zitat belegt ist
    
    Absatz: {paragraph_text}
    
    Überarbeiteter Absatz:

  dissertation_methodik: |
    Du bist ein hochqualifizierter KI-gestützter wissenschaftlicher Schreibassistent.
    Überarbeite den folgenden Absatz aus der Methodik einer Dissertation im APA-7-Stil.
    Stelle sicher, dass:
    - Technische Details präzise und vollständig sind
    - Alle Zitate im Format (Autor Jahr) korrekt sind
    - Der Text wissenschaftlich-formal und akademisch ist
    
    Absatz: {paragraph_text}
    
    Überarbeiteter Absatz:

  dissertation_ergebnisse: |
    Du bist ein hochqualifizierter KI-gestützter wissenschaftlicher Schreibassistent.
    Überarbeite den folgenden Absatz aus dem Ergebnisteil einer Dissertation im APA-7-Stil.
    Stelle sicher, dass:
    - Die Ergebnisse logisch nachvollziehbar dargestellt sind
    - Alle Zitate im Format (Autor Jahr) korrekt sind
    - Der Text wissenschaftlich-formal und akademisch ist
    
    Absatz: {paragraph_text}
    
    Überarbeiteter Absatz:

  dissertation_diskussion: |
    Du bist ein hochqualifizierter KI-gestützter wissenschaftlicher Schreibassistent.
    Überarbeite den folgenden Absatz aus der Diskussion einer Dissertation im APA-7-Stil.
    Stelle sicher, dass:
    - Die Einordnung in den Forschungskontext klar ist
    - Limitationen und Ausblick angemessen dargestellt sind
    - Alle Zitate im Format (Autor Jahr) korrekt sind
    - Der Text wissenschaftlich-formal und akademisch ist
    
    Absatz: {paragraph_text}
    
    Überarbeiteter Absatz:

  dissertation_literatur: |
    Du bist ein hochqualifizierter KI-gestützter wissenschaftlicher Schreibassistent.
    Überarbeite das folgende Literaturverzeichnis einer Dissertation im APA-7-Stil.
    Stelle sicher, dass:
    - Alle Einträge alphabetisch sortiert sind
    - Vollständige DOI-Angaben vorhanden sind
    - Das Format vollständig APA-7-konform ist
    
    Literaturverzeichnis: {paragraph_text}
    
    Überarbeitetes Literaturverzeichnis:
```

**`ci/ai-revision-config.yaml`:**

```yaml
files:
  matchings:
    - files:
        - ^.*abstract.*\.md$
        - ^.*Abstract.*\.md$
      prompt: dissertation_abstract
    - files:
        - ^.*einleitung.*\.md$
        - ^.*Einleitung.*\.md$
        - ^.*introduction.*\.md$
      prompt: dissertation_einleitung
    - files:
        - ^.*methodik.*\.md$
        - ^.*Methodik.*\.md$
        - ^.*methods.*\.md$
      prompt: dissertation_methodik
    - files:
        - ^.*ergebnisse.*\.md$
        - ^.*Ergebnisse.*\.md$
        - ^.*results.*\.md$
      prompt: dissertation_ergebnisse
    - files:
        - ^.*diskussion.*\.md$
        - ^.*Diskussion.*\.md$
        - ^.*discussion.*\.md$
      prompt: dissertation_diskussion
    - files:
        - ^.*literatur.*\.md$
        - ^.*Literatur.*\.md$
        - ^.*references.*\.md$
      prompt: dissertation_literatur
  default_prompt: dissertation_einleitung
```

### Option B: Eigenständiges Python-Skript für phasenweise Erstellung

Für die vollständige Erstellung einer Dissertation mit dem phasenweisen Ansatz können Sie ein eigenständiges Python-Skript verwenden. Siehe `examples/dissertation_generator.py` für ein vollständiges Beispiel.

## 4. Verfügbare Platzhalter

Beim Verwenden von Prompts mit manubot-ai-editor stehen folgende Platzhalter zur Verfügung:

- `{paragraph_text}`: Der Text des aktuellen Absatzes
- `{title}`: Der Titel des Manuskripts (aus `content/metadata.yaml`)
- `{keywords}`: Komma-getrennte Keywords des Manuskripts
- `{section_name}`: Der Name des Abschnitts (z.B. "abstract", "introduction", "results", "discussion", "methods")

## 5. Schnell-Checkliste

- [ ] System-Prompt exakt übernehmen (inkl. Rollen- und Stil-Definition).  
- [ ] Dein Thema und Ziel-Wortzahl im *User-Prompt* angeben.  
- [ ] Nach jeder Phase (Outline → Abstract → Kapitel) **prüfen & bestätigen**.  
- [ ] Für jede Aussage **mindestens einen PubMed-Citation-Eintrag** sicherstellen.  
- [ ] Am Ende das **Literaturverzeichnis** alphabetisch nach APA 7 formatieren.  
- [ ] Finales Dokument **eigenständig auf Plagiate und korrekte DOI-Angaben prüfen**.  

## 6. Weitere Ressourcen

- [Custom Prompts Dokumentation](custom-prompts.md) - Allgemeine Informationen zur Verwendung von benutzerdefinierten Prompts
- [Environment Variables](env-vars.md) - Verfügbare Umgebungsvariablen für die Konfiguration
- [Beispiel-Skript](../examples/dissertation_generator.py) - Vollständiges Python-Skript für die phasenweise Dissertation-Erstellung

---

**Hinweis:** Dieses Prompt-Design ist als Best Practice für die Erstellung von Dissertationen gedacht. Für die Überarbeitung bestehender Manuskripte verwenden Sie bitte die Standard-Prompts oder die oben beschriebenen Konfigurationsdateien.

