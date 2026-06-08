# Obsidian Note Standard

## Note architecture

Use this default structure:

```text
<Domain>/
├── 00 <Domain> 知识地图.md
├── Lectures/
│   ├── 01 <Detailed chapter>.md
│   ├── 02 <Detailed chapter>.md
│   └── ...
├── 01 <Concept card>.md
├── 02 <Concept card>.md
├── ...
├── 10 <Terminology or comparison>.md
├── <Source title> 原始材料.md
├── <Domain> 知识图谱.canvas
└── attachments/
    └── <clean source filename>
```

## Frontmatter

Use only useful metadata:

```yaml
---
aliases:
  - English Name
tags:
  - domain/category
  - course/or-source
source: "[[Source note]]"
---
```

Do not add decorative metadata that the vault does not use.

## MOC contents

The MOC should contain:

1. One-sentence core pipeline or thesis.
2. Numbered learning route linking every concept note.
3. Mermaid architecture or concept flow when useful.
4. A comparison of major method families.
5. Important distinctions and caveats.
6. Links to the source note and attachment.

The primary learning route must point to `Lectures/` first. Concept cards are for lookup and graph navigation, not the default substitute for a chapter.

## Detailed lecture chapter

A chapter should read like teaching material:

1. Motivation and the problem being solved.
2. Prerequisites and connection to the previous chapter.
3. Concepts introduced in a deliberate sequence.
4. One or more worked examples.
5. Formula derivation, algorithm trace, or tensor-shape trace.
6. Training/inference distinction when relevant.
7. Common mistakes and misconceptions.
8. Limitations, trade-offs, and when to use the method.
9. Key English wording with Chinese explanation.
10. Summary and self-check questions.

Use connected prose between lists and formulas. A chapter that is only a definition table, formula list, or bullet outline is incomplete.

## Concept card

A concept card should:

- state the definition precisely
- preserve notation and terminology
- summarize mechanism and trade-offs
- link to the detailed chapter where it is explained
- link laterally to comparable concepts

It may be concise because the lecture chapter supplies depth.

## Bilingual pattern

Preferred:

```markdown
知识图谱嵌入（Knowledge Graph Embedding, KGE）...

**Key English**

> Pass every literal value as a query parameter.
```

Avoid:

- translating code identifiers
- English paragraphs with no Chinese explanation
- removing established acronyms
- retaining every sentence merely because it is English

## Linking pattern

Each concept note should link:

- upward to the MOC
- backward to prerequisites
- forward to applications or evaluation
- sideways to alternatives or comparisons

Use display aliases where they improve readability:

```markdown
[[03 Knowledge Graph Embedding|知识图谱嵌入]]
```

## Canvas standard

Canvas JSON must contain:

- `nodes`: file nodes with vault-relative `file` values
- `edges`: directed conceptual relationships
- readable coordinates without excessive overlap

Use a left-to-right or top-to-bottom main pipeline and place comparison/validation notes around it.

## Quality bar

The result should let the user:

- learn the topic in a sensible order
- find the original source
- recognize exact English terminology
- compare methods and understand limitations
- navigate by backlinks, Graph View, and Canvas
- distinguish source claims from general conclusions
- study a topic from motivation through worked examples without reopening the source slides
