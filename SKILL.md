---
name: obsidian-knowledge-ingest
description: Convert source files into a structured Obsidian knowledge domain with teaching notes in the user's chosen language, preserved original technical terminology and excerpts, Wikilinks, attachments, a Canvas knowledge map, and Graph View configuration. Use when the user provides one or more PDF, DOCX, PPTX, Markdown, text, notebook, or similar study/work files and names an Obsidian vault or destination folder, asking to organize, convert, import, summarize, or build a knowledge graph in Obsidian.
---

# Obsidian Knowledge Ingest

Turn source material into a usable linked textbook, not a glossary or a collection of compressed summaries. Work autonomously when the source files and destination are clear.

## Required Standard

Read [note-standard.md](references/note-standard.md) before writing notes.

Use the relevant installed document skill or bundled workspace dependencies to extract source content. For PDFs, use a structured PDF parser such as `pypdf`; ignore notebook installation logs and other low-value execution noise unless operationally important.

## Workflow

### 1. Resolve the destination

Confirm the supplied destination belongs to an Obsidian vault by locating its nearest parent `.obsidian` directory.

- Treat that directory's parent as the vault root.
- Treat the user-specified folder as the knowledge-domain destination.
- If the user names a vault but no subfolder, derive a concise domain folder from the source title.
- Do not write into a different vault based only on topical similarity.
- If multiple destinations are plausible and the user did not identify one, ask one concise question.

Inspect a small sample of existing Markdown notes and `.obsidian/graph.json` to learn language, naming, link, tag, and graph conventions. Preserve unrelated content and settings.

### 2. Extract and survey the source

Extract all useful text and metadata. Identify:

- document title and domain
- main sections and conceptual hierarchy
- definitions, formulas, workflows, architecture, code patterns, experiments, and results
- important English terms, exact technical names, acronyms, commands, query languages, and short high-value excerpts
- connections to existing vault notes
- low-value content to exclude, such as package installation output, repeated notebook output, progress bars, and stack traces with no conceptual value

Never copy secrets. Scan for API keys, passwords, tokens, connection strings, personal data, and credentials. Omit sensitive values and add a security warning when exposure is visible in the source.

### 3. Design a three-layer knowledge domain

Use three distinct layers. Do not make atomic notes carry the entire teaching burden.

1. **Map layer**
   - `00 <Topic> 知识地图.md`
   - learning routes, module overview, prerequisites, and Canvas entry
2. **Detailed lecture layer**
   - `Lectures/01 <Chapter>.md`, etc.
   - textbook-style explanations that preserve the source's teaching sequence
   - combine related slides into coherent chapters, but retain derivations, examples, and reasoning
3. **Concept layer**
   - concise numbered concept/reference notes at the domain root or under `Concepts/`
   - definitions, formulas, comparisons, and backlinks for Graph View navigation

Also create:

- one terminology/comparison/reference note when useful
- `<Source title> 原始材料.md`
- `attachments/` containing a copy of the original source
- `<Topic> 知识图谱.canvas`

For course slides or textbooks, prefer 4-10 detailed lecture chapters plus concept notes. For a single short source, one detailed lecture chapter may be enough. Do not compress dozens of source pages into a short concept card and call it complete.

Connect new notes to relevant existing vault notes. Avoid creating duplicate concepts when a strong existing note can be linked or safely enriched. Do not overwrite or substantially rewrite an existing note unless the user requested it.

### 4. Write detailed teaching chapters in the requested language

Use the language explicitly requested by the user. If the user does not specify one, follow the dominant language and writing style of the destination vault; if that is unclear, use the source's primary language.

Preserve terminology in its original language where it improves precision:

- technical term on first mention: translated explanation plus `Original Term, acronym` where useful
- exact model, framework, API, class, function, tool, command, and keyword names
- formulas and code/query syntax
- short, high-value original wording under `Key terminology`, `Original wording`, `Core definition`, or a callout

Explain preserved original-language terminology in the selected output language. Do not translate identifiers or established keywords. Do not paste long copyrighted passages; keep direct excerpts short and use paraphrase for the rest.

Every detailed lecture chapter should normally include:

- **Why this matters**: the problem or motivation before introducing terminology
- **Prerequisites**: concepts assumed from earlier chapters
- **Step-by-step explanation**: preserve the source's reasoning sequence
- **Worked example**: carry at least one concrete example through the mechanism or calculation
- **Derivation or shape trace**: explain formulas, variables, tensor/matrix shapes, or algorithm state transitions
- **Training vs inference** where relevant
- **Common mistakes and misconceptions**
- **Limitations and design trade-offs**
- **Connections** to prior and later chapters
- **Key terminology** definitions or short source wording, explained in the selected output language
- **Self-check questions** or a concise recap

Concept notes may be shorter, but should link to the detailed lecture section where the concept is taught.

Do not merely list bullets from slides. Convert them into connected explanatory prose. For mathematical or algorithmic material, explain each symbol and show at least one small numerical or textual example.

As a default depth target:

- substantial lecture source: roughly 1,200-3,000 Chinese characters, or an equivalent level of detail in the selected language, per chapter
- concept card: roughly 300-1,000 Chinese characters, or an equivalent level of detail in the selected language
- MOC: navigation and synthesis, not a replacement for chapters

Every concept note should include:

- a clear definition or central idea
- mechanism, workflow, or formula where relevant
- strengths, limitations, and practical implications where relevant
- links to prerequisites, related concepts, applications, and the MOC
- source caveats when results depend on a notebook run, dataset version, model version, or hyperparameters

### 5. Build the graph

Use `[[Wikilinks]]` extensively but meaningfully. Build both:

- a conceptual main chain, such as foundation → representation → method → training → evaluation → application
- lateral comparison links among related models, methods, or design choices

Create an Obsidian Canvas JSON file with file nodes and directed edges representing the learning architecture. Put detailed lecture chapters on the main path and concept cards around them. Keep it readable; large courses may use 15-30 nodes. Ensure every Canvas file path is relative to the vault root.

Update `.obsidian/graph.json` conservatively:

- preserve existing keys and color groups
- add tag-based color groups for the new domain
- enable tags and arrows when useful
- never replace unrelated graph settings

### 6. Attach the source

Copy the original file into the domain's `attachments/` folder with a clean stable filename. Embed or link it from the source note. Do not remove or alter the user's original file.

### 7. Validate

Run:

```bash
python3 scripts/validate_obsidian_domain.py \
  --vault "/absolute/path/to/vault" \
  --domain "/absolute/path/to/vault/domain-folder"
```

Resolve every new-note warning before finishing:

- unresolved Wikilinks
- missing attachments
- invalid Canvas JSON
- Canvas nodes pointing to missing files
- invalid `.obsidian/graph.json`
- likely secrets in Markdown

Existing unresolved links elsewhere in the vault are not part of this task. Report them only if they affect the new domain.

## Safety and Editing Rules

- Never store live secrets from source files.
- Never delete or move unrelated vault content.
- Never replace the whole Graph View config merely to add colors.
- Check for an existing destination before creating files. Merge carefully or choose a non-conflicting folder; ask if overwrite intent is unclear.
- Keep filenames stable, descriptive, and compatible with Obsidian.
- When upgrading an existing compact domain, preserve its concept notes and add or expand the detailed lecture layer. Update the MOC and Canvas so readers encounter lectures before glossary-style nodes.
- Complete extraction, writing, linking, attachment copy, Canvas creation, graph configuration, and validation in the same task.

## Completion Report

State:

- exact destination
- number of notes and Wikilinks
- Canvas node/edge counts
- whether attachments and Graph View were configured
- validation result
- any omitted sensitive information or important source limitations
