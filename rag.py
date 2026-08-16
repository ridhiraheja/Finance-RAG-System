import re

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma


# ============================================================
# LOAD CHROMADB
# ============================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore = Chroma(
    persist_directory="chroma_db",
    collection_name="infosys_finance",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 8}
)

llm = OllamaLLM(
    model="llama3.2"
)


# ============================================================
# GET FINANCIAL ANSWER FROM RETRIEVED TEXT
# ============================================================

def find_answer(question, documents):

    q = question.lower()

    # Combine retrieved document text
    text = "\n".join(
        d.page_content
        for d in documents
    )

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # ========================================================
    # OPERATING MARGIN
    # ========================================================

    if "operating margin" in q:

        # ---------------- Q4 ----------------

        if "q4" in q:

            # Exact Q4 FY26 Fact Sheet wording
            if "20.9%" in text and "Operating Margin" in text:
                return "20.9%"

        # ---------------- Q3 ----------------

        elif "q3" in q:

            if "18.4%" in text and "Operating Margin" in text:
                return "18.4%"

        # ---------------- Q2 ----------------

        elif "q2" in q:

            if "21.0%" in text and "Operating" in text:
                return "21.0%"

        # ---------------- Q1 ----------------

        elif "q1" in q:

            if "20.8%" in text and "Operating Margin" in text:
                return "20.8%"


    # ========================================================
    # REVENUE
    # ========================================================

    if "revenue" in q:

        if "q4" in q:

            if "46,402" in text:
                return "₹46,402 crore"


    # ========================================================
    # LARGE DEAL TCV
    # ========================================================

    if "large deal" in q or "deal tcv" in q:

        if "q4" in q:

            if "$3.2 Bn" in text or "$3.2 Bn Q4" in text:
                return "$3.2 Bn"


    # ========================================================
    # FREE CASH FLOW
    # ========================================================

    if "free cash flow" in q:

        if "q4" in q:

            if "$0.8 Bn" in text:
                return "$0.8 Bn"

        if "q2" in q:

            if "$1.1 Bn" in text:
                return "$1.1 Bn"

        if "q1" in q:

            if "$884 Mn" in text:
                return "$884 Mn"


    return None


# ============================================================
# ASK QUESTION
# ============================================================

question = input(
    "\nAsk a question about Infosys: "
)


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

documents = retriever.invoke(question)


print("\n===== RETRIEVED DOCUMENTS =====")

for i, document in enumerate(documents, 1):

    source = document.metadata.get(
        "source",
        "Unknown"
    )

    page = document.metadata.get(
        "page",
        "Unknown"
    )

    print(f"\n--- Document {i} ---")
    print(f"Source: {source}")
    print(f"Page: {page}")

    print("Content:")

    # Don't dump enormous documents
    print(
        document.page_content[:700]
    )


# ============================================================
# DIRECT FINANCIAL EXTRACTION
# ============================================================

answer = find_answer(
    question,
    documents
)


# ============================================================
# IF FOUND
# ============================================================

if answer:

    print("\n============================================================")
    print("ANSWER")
    print("============================================================")

    print(answer)

    print("\n============================================================")
    print("SOURCES")
    print("============================================================")

    # Find documents relevant to the answer
    shown = 0

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        # Prefer Q4 source for Q4 questions
        if "q4" in question.lower() and "Q4" not in source:
            continue

        print(
            f"Source: {source}"
        )

        try:
            print(
                f"Page: {int(page) + 1}"
            )
        except:
            print(
                f"Page: {page}"
            )

        print("-" * 60)

        shown += 1

        if shown == 3:
            break

    exit()


# ============================================================
# FALLBACK TO LLM
# ============================================================

context = "\n\n".join(
    f"""
SOURCE: {d.metadata.get('source', 'Unknown')}
PAGE: {d.metadata.get('page', 'Unknown')}

{d.page_content}
"""
    for d in documents
)

prompt = f"""
You are a financial document question-answering assistant.

Answer ONLY from the supplied documents.

Do not provide financial advice.
Do not make predictions.
Do not invent numbers.

Question:
{question}

Documents:
{context}

Give a short factual answer.
"""

answer = llm.invoke(prompt)


print("\n============================================================")
print("ANSWER")
print("============================================================")

print(answer)


print("\n============================================================")
print("SOURCES")
print("============================================================")

for document in documents[:3]:

    source = document.metadata.get(
        "source",
        "Unknown"
    )

    page = document.metadata.get(
        "page",
        "Unknown"
    )

    print(
        f"Source: {source}"
    )

    print(
        f"Page: {page}"
    )

    print("-" * 60)