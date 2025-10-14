# Knowledge RAG API# Knowledge RAG API



A sophisticated Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions with intelligent, grounded responses powered by Google's Gemini AI and advanced text processing techniques.A compact Retrieval-Augmented Generation (RAG) system that lets you **upload a PDF/TXT** and **ask questions**. Answers are **strictly grounded** in the uploaded content and synthesized by **Google Gemini** with citations.



## Features---



### Core Functionality## Features



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

- **Health Monitoring**: Built-in health checks and debug endpoints│ ├── app.py # FastAPI app: /healthz, /upload, /ask (+ optional /query)

│ ├── rag_pipeline.py # (optional) Multi-doc FAISS RAG pipeline

## Project Structure│ ├── rerank.py # (optional) MMR reranker (multi-doc)

│ ├── settings.py # Configuration

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

- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))### 1) Create & activate a virtual environment

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

### API Endpoints

#### Health Check

```bash
GET /healthz
```

Response:
```json
{
  "ok": true,
  "message": "healthy"
}
```

#### Upload Document

```bash
POST /upload
Content-Type: multipart/form-data
File: document.pdf or document.txt
```

Response:
```json
{
  "session_id": "unique-session-id",
  "message": "Document uploaded and indexed successfully",
  "chunks": 15,
  "filename": "document.pdf"
}
```

#### Ask Question

```bash
POST /ask
Content-Type: application/json

{
  "session_id": "unique-session-id",
  "q": "What is the refund policy?",
  "k": 4,
  "strict": true
}
```

Response:
```json
{
  "answer": "The company offers a 30-day money-back guarantee on all products [1]. To request a refund, customers must provide the original receipt [1]. Refunds are processed within 5-7 business days [1].",
  "session_id": "unique-session-id",
  "question": "What is the refund policy?",
  "retrieved_blocks": [...],
  "filename": "document.pdf"
}
```

#### Debug Models (Development)

```bash
GET /debug/models
```

Lists available Gemini models.

### Query Examples

#### Specific Questions
- "What is the refund policy?"
- "How do I reset my password?"
- "What are the business hours?"

#### Document Overview
- "What is this document about?"
- "Give me a summary of the document"

#### Short/Fuzzy Queries
- "refund" → Enhanced to "refund policy return"
- "pasword" → Corrected to "password"
- "hrs" → Expanded to "hours business"

## Testing

### Web Interface Testing (Recommended)

1. Open `tester.html` in your browser
2. Upload a PDF or TXT document
3. Test various question types:
   - **Specific Questions**: "What is the refund policy?"
   - **Document Overview**: "What is this document about?"
   - **How-to Questions**: "How do I reset my password?"

### API Testing with curl

```bash
# Upload a document
curl -X POST "http://localhost:8000/upload" -F "file=@your_document.pdf"

# Ask questions (use session_id from upload response)
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"your-session-id","q":"What is the refund policy?","k":4,"strict":true}'
```

## Architecture

### RAG Pipeline

1. **Document Processing**:
   - PDF/TXT extraction using pypdf
   - Text chunking with overlap for context preservation (220 words, 40 word overlap)
   - TF-IDF vectorization with n-gram support (1-2 words)

2. **Query Processing**:
   - Fuzzy correction for typos using difflib
   - Synonym expansion for short queries
   - Dynamic parameter adjustment based on query length

3. **Retrieval & Generation**:
   - TF-IDF cosine similarity for relevant chunk retrieval (max 4 chunks)
   - Limited context (4 blocks, 1600 characters)
   - Google Gemini AI for natural language generation (160 tokens max)
   - Strict grounding validation with citation requirements
   - Fallback to "I don't know" for out-of-scope queries

### Key Components

#### `backend/app.py` - Main Application
- FastAPI server with CORS support
- Session-based document management
- Single-document TF-IDF + Gemini implementation
- Strict answer grounding with citation validation
- Enhanced query processing (fuzzy, n-gram, synonyms)

#### `backend/rag_pipeline.py` - Multi-Document RAG
- FAISS vector store integration
- Sentence transformer embeddings
- Advanced retrieval and reranking

#### Answer Generation
- **Max Context**: 4 blocks, 1600 characters
- **Max Tokens**: 160 (ensures concise answers)
- **Temperature**: 0.1 (consistent, deterministic)
- **Citation Requirement**: Every sentence must have [n]
- **Validation**: 30% token overlap + citations required

## Security & Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Required for Gemini AI integration
- `GEMINI_MODEL`: Specify model version (default: models/gemini-2.0-flash)
- `HOST`/`PORT`: Server configuration

### Data Privacy

- Session-based isolation prevents cross-document leakage
- Temporary storage with configurable cleanup
- No persistent storage of sensitive content
- `.env` file excluded from git (in `.gitignore`)

## Production Considerations

### Scaling

- Consider Redis for session management in multi-instance deployments
- Implement proper rate limiting for API endpoints
- Add authentication and authorization layers

### Monitoring

- Built-in health checks at `/healthz`
- Debug endpoints for development (`/debug/models`)
- Comprehensive error handling with fallbacks

### Performance

- Efficient TF-IDF caching per session
- Optimized chunk retrieval with configurable top-k (max 4)
- Compact context for faster response times

## Key Improvements

### Strict Grounding System

✅ **Concise Answers**: 1-4 sentences maximum  
✅ **Required Citations**: Every sentence must include [n]  
✅ **Limited Context**: 4 blocks, 1600 chars (prevents content dumps)  
✅ **Token Limit**: 160 tokens (ensures brevity)  
✅ **Validation**: Strict overlap checking + citation verification  

### Before vs After

**Before:**
```
[Dumps 500+ characters of raw content without structure...]
```

**After:**
```
The company offers a 30-day money-back guarantee on all products [1]. 
To request a refund, customers must provide the original receipt [1]. 
Refunds are processed within 5-7 business days [1].
```

## Documentation

Additional documentation available:

- `QUICK_REFERENCE.md` - Quick setup and usage guide
- `TEST_RESULTS.md` - Verified test results
- `FINAL_FIX.md` - Technical details of improvements
- `TESTING_GUIDE.md` - Comprehensive testing instructions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests for new features
4. Ensure all existing tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with FastAPI for high-performance API development
- Powered by Google Gemini AI for natural language generation
- Uses scikit-learn for efficient text processing
- Enhanced with sentence-transformers for semantic search

---

**Ready to get started?** Upload a document via `tester.html` and ask your first question! 🚀
