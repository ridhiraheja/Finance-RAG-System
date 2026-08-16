# Finance RAG System – Infosys Quarterly Reports

A local Retrieval-Augmented Generation (RAG) system for asking questions about Infosys quarterly financial reports.

The project uses Ollama for local AI processing, ChromaDB for vector storage and retrieval, LangChain for the RAG pipeline, and Streamlit for the user interface.

## Features

- Processes Infosys quarterly financial reports
- PDF document processing
- Document chunking
- Semantic search using ChromaDB
- Ollama embeddings using `nomic-embed-text`
- Local LLM using `llama3.2`
- Financial question answering
- Quarter-specific retrieval
- Source and page references
- Interactive Streamlit interface
- No OpenAI API key required

## System Architecture

```text
Infosys Quarterly Reports
          |
          v
      PDF Loading
          |
          v
  Document Processing
          |
          v
       Chunking
          |
          v
 Ollama Embeddings
 (nomic-embed-text)
          |
          v
       ChromaDB
          |
          v
 Relevant Retrieval
          |
          v
Financial Answer Extraction
          |
          v
     Ollama LLM
       llama3.2
          |
          v
     Streamlit UI
          |
          v
    Answer + Sources
