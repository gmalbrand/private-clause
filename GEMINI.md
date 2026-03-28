# 🛡️ PrivateClause

## 🛑 STRICT OPERATIONAL RULES
- **NEVER** execute a shell command (`pip`, `touch`, `mkdir`, etc.) without displaying the full command and waiting for a `(y/n)` confirmation.
- **NEVER** modify or create a file without first showing a summary of the changes.
- **ENVIRONMENT:** We are using a `.venv` for Python. Do not attempt to install packages globally.

## 🛠 MODES OF OPERATION
Gemini, you must follow these gated protocols:

<PROTOCOL:PLAN>
1. When a task is complex, enter PLAN mode first.
2. List all intended file changes and terminal commands.
3. STOP and ask: "Do you approve this plan?"
</PROTOCOL:PLAN>

<PROTOCOL:IMPLEMENT>
1. Only move to IMPLEMENT mode after I type "Approved" or "y".
2. Execute one step at a time.
3. If a command fails, STOP and wait for my instruction. Do not "Auto-fix."
</PROTOCOL:IMPLEMENT>

**PrivateClause** is an Agentic RAG (Retrieval-Augmented Generation) system specifically designed for deep reasoning over sensitive legal documents, like employment contracts, within a private infrastructure. It prioritizes data privacy and local-first AI engineering.

## 🏗️ Project Overview
- **Purpose:** Securely analyze and compare policies across multiple legal contracts without leaking data to third-party APIs.
- **Inference Engine:** [Ollama](https://ollama.com/) (running Llama 3.1/3.2 and Gemma models).
- **Orchestration:** [LlamaIndex](https://www.llamaindex.ai/) for document ingestion, metadata extraction, and agentic routing.
- **Storage:** [Neo4j](https://neo4j.com/) as both a Graph Store and Vector Database.
- **Architecture:** Local-first, CPU-optimized, and accessible via SSH tunneling for high security.

## 🚀 Building and Running

### 1. Prerequisites
- Python 3.10+
- Docker & Docker Compose (for Neo4j and Ollama)
- [Ollama](https://ollama.com/) (if running locally without Docker)

### 2. Setup Infrastructure
Start the core services (Neo4j and Ollama):
```bash
docker-compose up -d
```

### 3. Installation
Install the project in editable mode with development dependencies:
```bash
pip install -e ".[dev]"
```

### 4. Key Commands
The project provides a CLI entry point: `private-clause`.
- **Verify Setup:** Ensure Ollama and Neo4j are reachable.
  ```bash
  private-clause init
  ```
- **Load Documents:** Ingest PDFs from a directory into the Neo4j store.
  ```bash
  private-clause load --data-dir /path/to/your/docs
  ```
- **Configuration:** Use arguments like `--ollama-host`, `--neo4j-host`, and `--model` to override defaults.

## 🛠️ Development Conventions

- **Coding Style:** Adheres to modern Python standards. Uses `black` for formatting and `ruff` for linting.
- **Type Safety:** Leverages `pydantic` for data validation and schema management.
- **Testing:** `pytest` is included as a dev dependency. (TODO: Implement automated test suite).
- **Logging:** Uses standard Python `logging`. Use the `--debug` flag in the CLI for detailed output.
- **Environment Variables:** Managed via `.env` (using `python-dotenv`).

## 📁 Key Files
- `src/private_clause/main.py`: Main CLI entry point and orchestration logic.
- `src/private_clause/documents.py`: Logic for document ingestion and metadata extraction.
- `src/private_clause/neo4j_setup.py`: Neo4j connectivity and graph/vector store initialization.
- `src/private_clause/ollama_setup.py`: Logic for pulling models and checking Ollama status.
- `docker-compose.yml`: Defines the infrastructure for Neo4j and Ollama.
- `pyproject.toml`: Project metadata and dependency management.
