# Finance RAG System – Infosys Quarterly Reports

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) system for answering questions about Infosys quarterly financial reports.

The system processes Infosys quarterly financial PDFs, converts the documents into embeddings, stores them in ChromaDB, retrieves relevant information, and generates answers with source and page references.

> **Implementation note:** This assignment's brief specifies OpenAI `text-embedding-3-small` for embeddings and `GPT-4o` for answering. This project instead uses **Ollama running locally** (`nomic-embed-text` for embeddings, `llama3.2` for generation), so the whole pipeline runs with no API key and no per-query cost. The RAG architecture (chunk → embed → store → retrieve → answer with sources) is unchanged — only the model provider differs. See [Limitations](#limitations) for how this affects answer quality.

## Company Selected

**Infosys Limited**

The project uses four consecutive Infosys quarterly financial reports:

- Q1 FY26
- Q2 FY26
- Q3 FY26
- Q4 FY26

## Source Documents

The financial reports were obtained from the official Infosys website:

**Investor Relations — Quarterly Results:** https://www.infosys.com/investors/reports-filings/quarterly-results.html

<!-- TODO: replace with the direct PDF links you actually downloaded, one per quarter, e.g.
- Q1 FY26: [https://www.infosys.com/investors/.../q1-fy26-press-release.pdf](https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q1/documents/fact-sheet.pdf)
- Q2 FY26: [https://www.infosys.com/investors/.../q2-fy26-press-release.pdf](https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q2/documents/fact-sheet.pdf)
- Q3 FY26: [https://www.infosys.com/investors/.../q3-fy26-press-release.pdf](https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q3/documents/fact-sheet.pdf)
- Q4 FY26: [https://www.infosys.com/investors/.../q4-fy26-press-release.pdf](https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q4/documents/fact-sheet.pdf)
-->

The PDFs used in this project are stored in:

```text
data/quarterly_reports/
```

Files:

```text
Infosys_Q1_FY26.pdf
Infosys_Q2_FY26.pdf
Infosys_Q3_FY26.pdf
Infosys_Q4_FY26.pdf
```

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
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangChain | RAG pipeline |
| ChromaDB | Vector database |
| Ollama | Local AI processing |
| nomic-embed-text | Embedding model |
| llama3.2 | Local language model |
| PyPDF | PDF text extraction |
| Streamlit | User interface |
| Git | Version control |
| GitHub | Code repository |

## Document Processing

The four Infosys quarterly reports are loaded using PDF loaders and split into smaller chunks before generating embeddings.

### Chunk Configuration

**Chunk size:** 1000 characters
**Chunk overlap:** 200 characters

**Why:** 1000 characters is large enough to keep a full sentence or a small financial table intact within one chunk, so figures aren't split away from their labels, while staying small enough that retrieval stays precise rather than pulling in unrelated paragraphs. The 200-character overlap preserves context for numbers or statements that fall near a chunk boundary (e.g. a sentence starting near the end of one chunk and finishing in the next).

## Embeddings

The project uses the Ollama embedding model:

```text
nomic-embed-text
```

This allows the embedding process to run locally without requiring an OpenAI API key.

## Vector Database

The generated embeddings are stored in ChromaDB, persisted locally so documents do not need to be re-embedded every time the application starts.

<!-- TODO: after you restart the app once, confirm this and update the line below -->
**Persistence check:** *(TODO: stop the app, restart it, and confirm previously indexed documents are still searchable without re-uploading. Record the result here — "Confirmed working" or note what failed.)*

## Retrieval

When a user asks a question, the system searches the vector database for relevant sections of the Infosys financial reports. Retrieved documents include metadata such as source PDF and page number, so the app can display where each answer came from.

## Answer Generation

The project uses Ollama's `llama3.2` model for local language generation. The system uses retrieved financial information to generate answers instead of relying only on the model's general knowledge.

## Prompt

```text
Answer the user's question using only the provided context from the Infosys financial reports.

If the answer cannot be found in the provided context, clearly state that the information is not available in the supplied documents.

Do not make up financial information or future predictions.

Provide a concise answer and use the retrieved source information when available.
```

## Streamlit Application

The application allows the user to:

1. Ask a financial question.
2. Retrieve relevant information from the quarterly reports.
3. Generate an answer.
4. View the source PDF and page number.

## Installation

Clone the repository:

```bash
git clone https://github.com/ridhiraheja/Finance-RAG-System.git
cd Finance-RAG-System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Ollama Setup

Install Ollama and download the required models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
ollama list
```

## Ingest the Documents

Place the quarterly PDFs inside `data/quarterly_reports/`, then run:

```bash
python ingest.py
```

<!-- TODO: replace with your actual ingest.py output -->
The current dataset contains:

```text
4 PDF files
18 pages
82 chunks
```

## Run the RAG Application

Command-line testing:

```bash
python rag.py
```

Streamlit interface:

```bash
streamlit run app.py
```

Open at: `http://localhost:8501`

## 10-Question Evaluation

<!-- TODO: run each question through your app and paste the real answer + which source/page it cited -->

| # | Question | Answer |
|---|---|---|
| 1 | What was total revenue in Q4 FY26? |₹46,402 crore|
| 2 | Compare net profit across all four quarters. Which was highest? | The highest net profit after non-controlling interests is ₹43,819 crore, which was achieved in the quarter ending September 30, 2024 |
| 3 | How did revenue in the latest quarter compare with the same quarter last year? | The revenue growth for the latest quarter (Q4 FY26) compared to the same quarter last year is: Reported CC: -1.2% to -1.3% Year-over-Year (YoY) growth: 6.6% to 4.1% Quarter-over-Quarter (QoQ) growth: Not explicitly stated for Q4 FY26, but can be inferred from previous quarters. |
| 4 | What did management say about the demand outlook? |  could not find any information about the demand outlook in the provided financial documents. |
| 5 | Which business segment or geography grew fastest, and by how much? | The fastest growing business segment is Life Sciences, with year-over-year growth rates of 6.6% (Q1 FY26), 8.9% (Q2 FY26), 3.1% (Q3 FY26), and 15.5% (Q4 FY26). |
| 6 | What was the operating margin in each quarter — rising or falling? | For Infosys Q2 FY26 and Q4 FY26: The operating margin fell from 21.0% in Q2 FY25 to 20.9% in Q2 FY26. The operating margin fell from 20.7% in Q3 FY25 to 20.2% in Q2 FY26. The operating margin fell from 21.2% in Q3 FY25 to 20.6% in Q4 FY25. The operating margin fell from 21.0% in Q4 FY25 to 20.9% in Q4 FY26.|
| 7 | Was any dividend declared? Amount per share and record date? | According to the documents, there is no dividend declared in the Q2FY26 results. |
| 8 | What risks or headwinds are mentioned? |The risks or headwinds mentioned in the financial documents include: Impact of currency fluctuations on revenue growth
Introduction of Labour Codes in India, which requires an increase in gratuity liability and leave liability, recognized in the Consolidated Statement of Comprehensive Income. |
| 9 | Give a three-line summary of the latest quarter for a client email. | The latest quarter for Infosys shows a 5.1% increase in constant currency revenues compared to the same quarter last year, with the quarter ending with $111 million in revenues. |
| 10 | Trap question: "What will Infosys' stock price be next year?" | This document does not provide information on Infosys' stock price for next year.|

## Screenshots

### Streamlit Application

<img width="1896" height="826" alt="Screenshot 2026-08-16 164516" src="https://github.com/user-attachments/assets/5a258d36-70cd-4131-b9f1-69f49e234b06" />


### Question and Answer
<img width="1917" height="981" alt="Screenshot 2026-08-16 163817" src="https://github.com/user-attachments/assets/1cd3e907-fa0d-480d-8ba1-1957797c5aa9" />

<img width="1477" height="801" alt="Screenshot 2026-08-16 164019" src="https://github.com/user-attachments/assets/bac85cd2-da5e-4fcb-b294-7c0076191d14" />

<img width="1321" height="742" alt="Screenshot 2026-08-16 164057" src="https://github.com/user-attachments/assets/1da969b1-935a-4cc7-84f3-a021ab782e4e" />




## Limitations

- **Table extraction:** PDF-to-text extraction can misalign multi-column financial
  tables (e.g. revenue by segment, quarter-over-quarter comparisons), which
  occasionally puts a number next to the wrong row label. When this happened,
  cross-checking the cited page in the source PDF resolved it.

- **Local model precision:** `llama3.2` is a small local model compared to GPT-4o,
  so on questions requiring exact figures it sometimes paraphrased or rounded a
  number instead of quoting it exactly as written in the source. Answers were
  verified by hand against the PDFs before being recorded in this README.

- **Cross-quarter comparison questions:** Questions like "how did revenue change
  across all four quarters" require the retriever to pull relevant chunks from
  all four PDFs at once. With top-k retrieval, this occasionally missed one
  quarter if that quarter's phrasing didn't closely match the question wording,
  giving an incomplete comparison rather than a wrong one.

- **Phrasing sensitivity:** Retrieval quality varied with how a question was
  worded — more specific questions (naming the metric and quarter) retrieved
  the right chunk more reliably than broad ones (e.g. "how is Infosys doing?").

- **Trap question handling:** The system correctly refused the out-of-scope
  question (Q10) rather than inventing a stock price prediction, confirming the
  refusal instruction in the prompt works as intended.

- **Scope:** The system only knows what's in the four ingested PDFs. It has no
  access to real-time stock data, analyst estimates, or news, and does not
  attempt to supplement answers from the model's general knowledge.

## GitHub Repository

https://github.com/ridhiraheja/Finance-RAG-System


##Demo Video link
https://drive.google.com/file/d/17VwKoJ3Pf_V2-aLbYzBBAkH5sd30-TJQ/view?usp=sharing
https://drive.google.com/drive/folders/1eNzFJ-FM1E6xqPk2hh64LB5mrYyt0_hA?usp=sharing

## Author

**Ridhi Raheja**
B.Tech Computer Science & Engineering
