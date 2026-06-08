# Obsidian Knowledge Ingest

A Codex skill that converts PDFs, slides, documents, notebooks, and other source files into a structured Obsidian knowledge domain.

它不是把材料压缩成术语表，而是生成一套可以连续学习的三层知识结构：

1. **Map layer**：知识地图、学习路线与 Canvas 入口
2. **Detailed lecture layer**：教材式中文讲义，保留关键英文术语、公式、示例和推导
3. **Concept layer**：适合双链、检索和 Graph View 的原子概念卡

## Features

- Detects the target Obsidian vault and follows its existing conventions
- Creates detailed teaching chapters instead of short slide summaries
- Preserves important English terminology, identifiers, formulas, and short excerpts
- Adds meaningful `[[Wikilinks]]` across chapters and concept notes
- Copies original source files into `attachments/`
- Builds an Obsidian Canvas knowledge map
- Updates Graph View configuration conservatively
- Validates links, Canvas references, attachments, graph configuration, lecture depth, and likely secrets

## Generated Structure

```text
<Domain>/
├── 00 <Domain> 知识地图.md
├── Lectures/
│   ├── 01 <Detailed chapter>.md
│   └── ...
├── 01 <Concept card>.md
├── ...
├── <Source title> 原始材料.md
├── <Domain> 知识图谱.canvas
└── attachments/
    └── <source file>
```

## Installation

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/leoohuang/obsidian-knowledge-ingest.git \
  ~/.codex/skills/obsidian-knowledge-ingest
```

Restart Codex if the skill is not discovered immediately.

## Usage

Provide the source file and the destination Obsidian folder:

```text
Use $obsidian-knowledge-ingest to organize these course slides into
/path/to/MyVault/NLP. Preserve key English terminology and build a knowledge graph.
```

中文示例：

```text
把这个 PDF 按知识点整理到 Obsidian 的 NLP 文件夹。
保留关键英文术语，生成详细讲义、概念卡和 Canvas 知识图谱。
```

## Validation

The included validator can also be run manually:

```bash
python3 scripts/validate_obsidian_domain.py \
  --vault "/absolute/path/to/vault" \
  --domain "/absolute/path/to/vault/domain-folder"
```

## Requirements

- Codex with local skill support
- Python 3.10+
- An existing Obsidian vault with a `.obsidian/` directory
- Suitable local document extraction dependencies for the supplied file formats

## License

MIT
