# Obsidian Knowledge Ingest

A Codex skill that converts PDFs, slides, documents, notebooks, and other source files into a structured Obsidian knowledge domain.

## 中文简介

**Obsidian Knowledge Ingest** 是一个面向 Codex 的知识整理 Skill。你只需要提供 PDF、PPT、Word、Markdown、Notebook 等学习或工作资料，并指定一个 Obsidian 文件夹，它就会自动完成内容提取、知识重组、笔记撰写、双链连接、原始附件归档以及知识图谱构建。

它适合整理课程讲义、技术文档、研究报告、实验 Notebook 和企业内部材料。与普通的“PDF 总结”不同，这个 Skill 不会把几十页内容压缩成几条术语解释，而是尽量保留原材料的教学顺序、推理过程、公式、代码、案例、实验结果和关键英文表述，将其改写成可以连续学习和长期维护的 Obsidian 知识库。

生成的知识域采用三层结构：

1. **Map layer**：知识地图、学习路线与 Canvas 入口
2. **Detailed lecture layer**：教材式中文讲义，保留关键英文术语、公式、示例和推导
3. **Concept layer**：适合双链、检索和 Graph View 的原子概念卡

处理完成后，你会得到：

- 按推荐顺序组织的详细中文讲义
- 保留专业英文术语、模型名称、API、公式与代码的双语笔记
- 可独立检索和复习的概念卡
- 连接前置知识、相关方法、对比模型和应用场景的 `[[Wikilinks]]`
- 可视化展示学习路径的 Obsidian Canvas
- 归档在 `attachments/` 中的原始资料
- 自动检查失效链接、缺失附件、Canvas 引用、讲义深度和潜在敏感信息的验证工具

典型使用方式非常简单：

```text
把这些课程 slides 整理到我的 Obsidian/NLP 文件夹。
保留关键英文术语，内容尽可能详细，并构建知识图谱。
```

Skill 会自行识别 Obsidian Vault、参考已有笔记风格，并在不破坏原有内容和 Graph View 设置的前提下创建或扩充对应知识域。

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
