# Knowledge RAG API# Knowledge RAG API



A sophisticated Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions with intelligent, grounded responses powered by Google's Gemini AI and advanced text processing techniques.A compact Retrieval-Augmented Generation (RAG) system that lets you **upload a PDF/TXT** and **ask questions**. Answers are **strictly grounded** in the uploaded content and synthesized by **Google Gemini** with citations.

### Demo Video ([Get one here](https://drive.google.com/file/d/1XObPk4au5JGN_Cu4cuL_qh9l3LgBoGgq/view?usp=sharing))



### Features



### Core Functionality



- **Document Upload**: Support for PDF and TXT file uploads- **Upload & Ask**: `POST /upload` → `POST /ask`

- **Intelligent Q&A**: Ask questions about uploaded documents with contextual answers- **Strict grounding**: answers only from provided context; otherwise _“I don’t know based on the provided document.”_

- **Strict Grounding**: All answers are 1-4 sentences with required citations [1], [2]- **Smart query enhancement**: n-gram TF-IDF, typo/fuzzy handling, and synonym expansion for short queries

- **Session Management**: Per-upload session isolation for document queries- **Minimal UI**: `backend/static/tester.html` (served at `/`)

- **Smart Query Enhancement**: Handles typos, short queries, and synonym expansion- **Health monitoring**: `GET /healthz`

- **Optional multi-doc RAG**: FAISS index + MMR reranker + retrieval eval

### Advanced Features

---

- **Compact Context**: Limited to 4 blocks and 1600 characters for precise answers

- **Citation Requirements**: Every sentence must include [n] citations## Project Structure

- **Fuzzy Matching**: Automatic typo correction and query enhancement

- **N-gram TF-IDF**: Enhanced text matching with 1-2 word phrasesAssignment/

- **Strict Validation**: Ensures all answers are grounded in document content├── backend/ # Backend API and core logic



## Project Structure

```│ ├── init.py # Package init

-Knowledge-Base-Search-Engine-RAG-/│ └── data/ # (optional) Multi-doc data dirs

├── backend/                     # Backend API and core logic│ ├── raw/ # Raw files for multi-doc ingest

│   ├── app.py                  # Main FastAPI application│ ├── processed/ # Ingested chunks.jsonl

│   ├── rag_pipeline.py         # Multi-document FAISS RAG pipeline│ ├── uploaded/ # Per-session uploads (if persisted)

│   ├── settings.py             # Configuration settings│ └── index/ # Vector indices / meta

│   ├── __init__.py             # Package initialization├── backend/static/

│   └── data/                   # Data storage directories│ └── tester.html # Minimal web tester (served at /)

│       ├── raw/                # Raw uploaded files├── requirements.txt # Python dependencies

│       ├── processed/          # Processed document chunks├── .env.example # Environment template

│       ├── uploaded/           # Session-based uploads├── .gitignore

│       └── index/              # Vector indices└── README.md

├── tester.html                 # Web-based testing interface

├── requirements.txt            # Python dependenciesyaml

├── .env.example                # Environment configuration templateCopy code

├── .gitignore                  # Git exclusions

└── README.md                   # This documentation---

```

## 🔧 Installation & Setup

## Installation & Setup

### Prerequisites

### Prerequisites- Python **3.11+** (tested on 3.11/3.13)

- Google **Gemini** API key

- Python 3.8+ (developed with Python 3.13)

- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
### 1) Create & activate a virtual environment

```bash

### 1. Clone and Navigatepython -m venv .venv

# Windows

```bash.\.venv\Scripts\activate

git clone https://github.com/Abhishek15112003/-Knowledge-Base-Search-Engine-RAG-.git# Linux/Mac

cd -Knowledge-Base-Search-Engine-RAG-source .venv/bin/activate

```2) Install dependencies

bash

### 2. Install DependenciesCopy code

pip install -r requirements.txt

```bash3) Configure environment

# Create and activate virtual environmentCreate .env in the project root (or copy from .env.example):

python -m venv .venv

env

# WindowsCopy code

.venv\Scripts\activateAPP_NAME="Knowledge RAG API"

APP_ENV=dev

# Linux/MacHOST=0.0.0.0

source .venv/bin/activatePORT=8000



# Install packagesGOOGLE_API_KEY=your_gemini_api_key_here

pip install -r requirements.txt# Pick a model your account supports; examples:

```GEMINI_MODEL=gemini-1.5-flash

# alternatives: gemini-1.5-flash-001, gemini-1.5-flash-latest, gemini-1.5-pro

### 3. Environment ConfigurationWindows copy example: Copy-Item .env.example .env

Unix copy example: cp .env.example .env

Create `.env` file from template:

4) Run the API

```bashbash

cp .env.example .envCopy code

```uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload

Open:

Edit `.env` file:

Tester UI: http://localhost:8000/

```env

APP_NAME="Knowledge RAG API"Health: http://localhost:8000/healthz

APP_ENV=dev

HOST=0.0.0.0🚀 Usage

PORT=8000Web interface (recommended)

Visit http://localhost:8000/

# Get your API key from: https://makersuite.google.com/app/apikey

GOOGLE_API_KEY=your_api_key_hereUpload a .pdf or .txt



# Available models: models/gemini-2.0-flash, models/gemini-2.5-flash, models/gemini-2.5-proAsk a question (e.g., refund policy, password reset)
GEMINI_MODEL=models/gemini-2.0-flash
```

### 4. Start the Server

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## Usage

### Web Interface (Recommended for Testing)

1. Open `tester.html` in your browser
2. Upload a PDF or TXT file
3. Ask questions about the document content
4. Get concise, cited responses (1-4 sentences with [n] citations)


- Uses scikit-learn for efficient text processing
- Enhanced with sentence-transformers for semantic search

---

**Ready to get started?** Upload a document via `tester.html` and ask your first question! 
