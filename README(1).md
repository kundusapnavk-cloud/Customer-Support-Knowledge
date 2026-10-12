# Customer Support Knowledge RAG

A portfolio project for building a Retrieval-Augmented Generation (RAG) system that answers customer support questions using a structured support knowledge base.

## Project Goal

The final system should work like this:

```text
Customer Question
      ↓
Find Relevant Support Documents
      ↓
Retrieve Best Context
      ↓
LLM Generates Answer
      ↓
Answer + Sources
```

The goal is to make answers grounded in approved support documentation instead of relying only on the LLM's general knowledge.

## Project Phases

1. Dataset + document ingestion
2. Chunking + metadata
3. Embeddings + vector database
4. Retrieval
5. Answer generation + citations
6. Hybrid search + reranking + filtering
7. Evaluation + API/UI

## Current Phase

### Phase 1 — Dataset + Document Ingestion

In this phase, we are making Python able to read and structure the support documents.

The support documents are stored as Markdown files with YAML metadata.

Example:

```yaml
---
title: Refund Policy
category: billing
product: taskflow
plan: pro_business
source_type: policy
---
```

The ingestion pipeline converts each Markdown file into a structured Python object.

```text
Markdown File
      ↓
loader.py
      ↓
Read YAML Metadata
      ↓
Read Document Content
      ↓
SupportDocument Object
```

## Current Project Structure

```text
Customer Support Knowledge/
├── data/
│   ├── account/
│   ├── billing/
│   ├── integrations/
│   ├── policies/
│   ├── troubleshooting/
│   └── workspace/
│
├── src/
│   └── ingestion/
│       ├── __init__.py
│       ├── loader.py
│       └── models.py
│
├── test_ingestion.py
├── requirements.txt
└── README.md
```

## What Each File Does

### `src/ingestion/models.py`

Defines the structure of one support document inside Python.

Example fields:

```text
content
title
category
source_path
product
plan
last_updated
source_type
```

### `src/ingestion/loader.py`

Reads a Markdown file, extracts its YAML metadata and content, and converts it into a `SupportDocument`.

### `src/ingestion/__init__.py`

Marks the `ingestion` folder as a Python package.

### `test_ingestion.py`

Used to test whether the loader can correctly read a support document.

### `requirements.txt`

Stores the Python libraries required by the project.

Current dependency:

```text
PyYAML
```

PyYAML is used to read YAML metadata from the Markdown files.

## Setup

From the project root:

```powershell
pip install -r requirements.txt
```

Then test the ingestion code:

```powershell
python test_ingestion.py
```

## Current Objective

Before moving to Phase 2, confirm that Python can correctly load the support documents from the `data/` folder.

After that, the next step is:

**Phase 2 — Chunking + Metadata**

This will break support documents into smaller searchable pieces that can later be embedded and retrieved.
