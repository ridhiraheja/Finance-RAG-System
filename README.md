\# 💰 Finance RAG System – Infosys Quarterly Reports



A local Retrieval-Augmented Generation (RAG) system that allows users to ask questions about Infosys quarterly financial reports.



The system processes quarterly financial documents, stores their embeddings in ChromaDB, retrieves relevant information, and provides financial answers through an interactive Streamlit interface.



The project uses Ollama for local AI processing, so an OpenAI API key is not required.



\---



\## 🚀 Features



\- 📄 Processes Infosys quarterly financial reports

\- ✂️ Document processing and chunking

\- 🔎 Semantic retrieval using ChromaDB

\- 🧠 Retrieval-Augmented Generation workflow

\- 🤖 Local LLM processing using Ollama

\- 📊 Financial question answering

\- 📚 Source and page references

\- 🌐 Interactive Streamlit interface

\- 🔐 No OpenAI API key required



\---



\## 🏗️ System Architecture



```text

Infosys Quarterly Reports

&#x20;         |

&#x20;         v

&#x20;     PDF Loading

&#x20;         |

&#x20;         v

&#x20; Document Processing

&#x20;         |

&#x20;         v

&#x20;      Chunking

&#x20;         |

&#x20;         v

&#x20;Ollama Embeddings

&#x20;(nomic-embed-text)

&#x20;         |

&#x20;         v

&#x20;      ChromaDB

&#x20;         |

&#x20;         v

&#x20;Relevant Retrieval

&#x20;         |

&#x20;         v

Financial Answer Extraction

&#x20;         |

&#x20;         v

&#x20;    Ollama LLM

&#x20;      llama3.2

&#x20;         |

&#x20;         v

&#x20;    Streamlit UI

&#x20;         |

&#x20;         v

&#x20;   Answer + Sources

```

