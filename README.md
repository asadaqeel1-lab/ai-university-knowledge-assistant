# 🎓 AI University Knowledge Assistant — Agentic RAG

An AI-powered University Knowledge Assistant built using Retrieval-Augmented Generation (RAG).

The system allows users to upload documents and ask questions about their content using semantic search and a local LLM.

## 🚀 Features

- 📄 PDF and DOCX document processing
- ✂️ Document chunking
- 🧠 Hugging Face embeddings
- 🔎 Semantic search
- 🗄️ ChromaDB vector database
- 🤖 Ollama + Llama 3.2
- ⚡ FastAPI file upload API
- 📚 Multiple document support
- 🔗 Source-aware answers
- 🔒 Local AI processing

## 🏗️ Architecture

```text
User
 │
 ▼
Document Upload
 │
 ▼
FastAPI
 │
 ▼
Document Loader
 │
 ▼
Text Chunking
 │
 ▼
Hugging Face Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Retriever
 │
 ▼
Ollama / Llama 3.2
 │
 ▼
AI Answer