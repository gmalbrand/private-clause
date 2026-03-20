# 🛡️ PrivateClause

**PrivateClause** is an Agentic RAG (Retrieval-Augmented Generation) system designed to perform deep reasoning over sensitive employment contracts without ever letting data leave your private infrastructure.

Built with **LlamaIndex** and **Ollama**, this project demonstrates a "Local-First" approach to AI Engineering, running fully quantized models on standard cloud CPUs to balance performance, cost, and absolute data privacy.

---

## 🏗️ The Architecture
Unlike traditional AI apps that leak metadata to third-party APIs, **PrivateClause** operates within a hardened perimeter:

* **Inference Engine:** [Ollama](https://ollama.com/) running **Llama 3.1 (8B)** with 4-bit quantization.
* **Orchestration:** [LlamaIndex](https://www.llamaindex.ai/) for document ingestion, metadata extraction, and agentic routing.
* **Vector Store:** [ChromaDB](https://www.trychroma.com/) (Persistent local instance).
* **Infrastructure:** Google Cloud Platform (GCP) Compute Engine (`e2-standard-4`).
* **Access:** Securely managed via **SSH Tunneling** (no public HTTP ports exposed).

---

## 🛠️ Key Features
* **Zero-Knowledge RAG:** Contracts are processed locally. No data is sent to OpenAI, Anthropic, or Google Gemini.
* **Metadata-Aware Retrieval:** Automatically extracts and filters by `Employee Name`, `Vesting Schedule`, and `Notice Period`.
* **Agentic Reasoning:** Uses a sub-question query engine to compare policies across multiple contracts (e.g., *"Which departments have a non-compete longer than 6 months?"*).
* **CPU Optimized:** Engineered to run efficiently on 4 vCPUs using optimized GGUF models.

