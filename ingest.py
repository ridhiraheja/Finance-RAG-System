import os
import shutil

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# ============================================================
# CONFIG
# ============================================================

PDF_FOLDER = "data/quarterly_reports"
DB_DIR = "chroma_db"
COLLECTION_NAME = "infosys_finance"


# ============================================================
# FIND PDFs
# ============================================================

pdf_files = [
    os.path.join(PDF_FOLDER, f)
    for f in os.listdir(PDF_FOLDER)
    if f.lower().endswith(".pdf")
]

print(f"Found {len(pdf_files)} PDF files.")


if len(pdf_files) == 0:
    print("ERROR: No PDF files found.")
    exit()


# ============================================================
# LOAD PDFs
# ============================================================

documents = []

for pdf in pdf_files:

    print(f"Loading: {os.path.basename(pdf)}")

    loader = PyPDFLoader(pdf)

    pages = loader.load()

    documents.extend(pages)


print(f"Total pages loaded: {len(documents)}")


# ============================================================
# SPLIT DOCUMENTS
# ============================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")


if len(chunks) == 0:
    print("ERROR: No chunks created.")
    exit()


# ============================================================
# DELETE OLD DATABASE
# ============================================================

if os.path.exists(DB_DIR):

    print("Removing old ChromaDB...")

    shutil.rmtree(DB_DIR)


# ============================================================
# EMBEDDINGS
# ============================================================

print("Loading embedding model...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ============================================================
# CREATE CHROMA DATABASE
# ============================================================

print("Creating ChromaDB...")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_DIR,
    collection_name=COLLECTION_NAME
)


# ============================================================
# VERIFY DATABASE
# ============================================================

count = vectorstore._collection.count()

print()
print("============================================")
print("CHROMADB VERIFICATION")
print("============================================")
print(f"Documents stored in ChromaDB: {count}")


if count == 0:

    print("ERROR: ChromaDB is EMPTY!")
    exit()


print()
print("Documents successfully stored in ChromaDB!")
print("Ingestion completed successfully.")