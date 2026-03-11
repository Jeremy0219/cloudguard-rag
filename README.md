# 🔐 CloudGuard RAG Assistant

> An AI-powered Retrieval-Augmented Generation (RAG) pipeline for querying cloud security frameworks using Claude AI and Azure AI Search.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Claude](https://img.shields.io/badge/Anthropic-Claude-black?logo=anthropic)
![Azure AI Search](https://img.shields.io/badge/Azure-AI%20Search-0078D4?logo=microsoftazure)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

> 🚧 **This project is actively under development.** Core pipeline and documentation are being built out — check the [Roadmap](#️-roadmap) for progress.

---

## 📌 Overview

CloudGuard is a command-line RAG assistant that ingests cloud security framework documents — including the **Azure Security Benchmark**, **CIS Controls**, and **NIST SP 800-53** — and answers natural language questions grounded in those documents.

Instead of hallucinating generic security advice, CloudGuard retrieves the most relevant policy sections first, then generates precise, cited answers using Anthropic's Claude.

> 💡 **Architecture note:** This project uses Anthropic Claude for LLM and embeddings alongside Azure AI Search as the vector store — a deliberate multi-provider design. The pipeline is built to be swappable with Azure OpenAI when enterprise credentials are available, making it production-ready for Azure-native environments.

**Example queries:**
- *"What controls should I implement for privileged identity management in Azure?"*
- *"How does NIST 800-53 address audit logging requirements?"*
- *"What does the Azure Security Benchmark say about network segmentation?"*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User CLI Query                     │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│         sentence-transformers (local embeddings)     │
│              Embed the user's question               │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                 Azure AI Search                      │
│        Vector search over indexed doc chunks        │
└──────────────────────────┬──────────────────────────┘
                           │
                  Top-K relevant chunks
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│           Anthropic Claude (claude-sonnet-4-6)      │
│   Generate grounded answer from retrieved context   │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│          Rich CLI Output with source citations       │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Features

- **Document ingestion pipeline** — Automatically chunks and indexes PDF/text security frameworks
- **Vector search** — Semantic retrieval via Azure AI Search with cosine similarity
- **Grounded answers** — Claude generates responses strictly from retrieved context, with source citations
- **Multi-framework support** — Ingest multiple security docs and query across all of them
- **Rich CLI** — Clean, color-coded terminal output with source attribution

---

## 📋 Prerequisites

- Python 3.10+
- Anthropic API key — [get one here](https://console.anthropic.com/)
- Azure subscription with:
  - Azure AI Search resource (Free tier sufficient)
- Git

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Jeremy0219/cloudguard-rag.git
cd cloudguard-rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

```env
# Anthropic
ANTHROPIC_API_KEY=your_key_here

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://YOUR_SEARCH.search.windows.net
AZURE_SEARCH_API_KEY=your_key_here
AZURE_SEARCH_INDEX_NAME=cloudguard-index
```

### 5. Ingest documents

```bash
python ingest.py --docs ./docs/
```

This will chunk, embed, and index all documents in the `docs/` folder into Azure AI Search.

### 6. Run the assistant

```bash
python main.py
```

---

## 📁 Project Structure

**Current:**
```
cloudguard-rag/
├── .env.example            # Environment variable template
├── .gitignore
├── LICENSE
└── README.md
```

**Planned (in development):**
```
cloudguard-rag/
├── docs/                   # Security framework documents (PDF/TXT)
│   ├── azure-security-benchmark.pdf
│   ├── cis-controls-v8.pdf
│   └── nist-800-53.pdf
├── src/
│   ├── ingestor.py         # Document chunking + embedding + indexing
│   ├── retriever.py        # Azure AI Search vector retrieval
│   ├── generator.py        # Claude answer generation
│   └── cli.py              # Rich CLI interface
├── .env.example            # Environment variable template
├── ingest.py               # Ingestion entrypoint
├── main.py                 # Query entrypoint
├── requirements.txt
└── README.md
```

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| LLM | Anthropic Claude (claude-sonnet-4-6) |
| Embeddings | sentence-transformers (local) |
| Vector Store | Azure AI Search |
| PDF Parsing | pypdf |
| CLI UI | rich |
| Config | python-dotenv |

---

## 📸 Demo

*Screenshots and demo video coming soon*

---

## 🗺️ Roadmap

- [ ] Core RAG pipeline (ingest + retrieve + generate)
- [ ] Multi-document support
- [ ] Source citation in responses
- [ ] Web UI with Streamlit
- [ ] Azure deployment (Container App)
- [ ] Swap in Azure OpenAI when enterprise credentials available

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Jeremy Sanchez** — CS Student @ UTSA | Cybersecurity Concentration | CompTIA Security+ | AZ-900  
Internship: IT @ Caterpillar Inc.  
[LinkedIn](https://linkedin.com/in/jeremy-sanchez-004073339/) · [GitHub](https://github.com/Jeremy0219)
