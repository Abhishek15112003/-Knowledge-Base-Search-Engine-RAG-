# Knowledge RAG API# Knowledge RAG API 



A sophisticated Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions with intelligent, grounded responses powered by Google's Gemini AI and advanced text processing techniques.# 1) Create and activate a virtual environment



## FeaturesA sophisticated Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions with intelligent, grounded responses powered by Google's Gemini AI and advanced text processing techniques.python -m venv .venv



### Core Functionality# Windows: .venv\\Scripts\\activate

- **Document Upload**: Support for PDF and TXT file uploads

- **Intelligent Q&A**: Ask questions about uploaded documents with contextual answers
- ##  Features# Linux/Mac: source .venv/bin/activate

- **Dual RAG Architecture**: 

  - Single-document TF-IDF + Gemini for focused queries

  - Multi-document FAISS + Sentence Transformers for complex retrieval

- **Strict Grounding**: Ensures all answers are backed by document content with citations### Core Functionality

- **Smart Query Enhancement**: Handles typos, short queries, and synonym expansion

- **Document Upload**: Support for PDF and TXT file uploads# 2) Install dependencies

### Advanced Features

- **Fuzzy Matching**: Automatic typo correction and query enhancement- **Intelligent Q&A**: Ask questions about uploaded documents with contextual answerspip install -r requirements.txt

- **N-gram TF-IDF**: Enhanced text matching with 1-3 word phrases

- **Citation System**: All answers include numbered citations `[1]`, `[2]` referencing source blocks- **Dual RAG Architecture**: 

- **Session Management**: Per-upload session isolation for document queries

- **Summary Generation**: Can provide document summaries and content overviews  - Single-document TF-IDF + Gemini for focused queries

- **Health Monitoring**: Built-in health checks and debug endpoints

  - Multi-document FAISS + Sentence Transformers for complex retrieval# 3) Configure env

## Project Structure

- **Strict Grounding**: Ensures all answers are backed by document content with citationscp .env.example .env

```

d:/Assignment/- **Smart Query Enhancement**: Handles typos, short queries, and synonym expansion

├── backend/                     # Backend API and core logic

│   ├── app.py                  # Main FastAPI application

│   ├── rag_pipeline.py         # Multi-document FAISS RAG pipeline

│   ├── settings.py             # Configuration settings### Advanced Features# 4) Run the API

│   ├── __init__.py             # Package initialization

│   └── data/                   # Data storage directories- **Fuzzy Matching**: Automatic typo correction and query enhancementuvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

│       ├── raw/                # Raw uploaded files- **N-gram TF-IDF**: Enhanced text matching with 1-3 word phrases

│       ├── processed/          # Processed document chunks- **Citation System**: All answers include numbered citations `[1]`, `[2]` referencing source blocks

│       ├── uploaded/           # Session-based uploads- **Session Management**: Per-upload session isolation for document queries

│       └── index/              # Vector indices- **Summary Generation**: Can provide document summaries and content overviews

├── tester.html                 # Web-based testing interface- **Health Monitoring**: Built-in health checks and debug endpoints

├── requirements.txt            # Python dependencies

├── .env.example                # Environment configuration template## Project Structure

├── .gitignore                  # Git exclusions

└── README.md                   # This documentation```

d:/Assignment/

├── backend/                     # Backend API and core logic

## Installation & Setup│
├── app.py                  # Main FastAPI application

│   ├── rag_pipeline.py         # Multi-document FAISS RAG pipeline

### Prerequisites│
├── settings.py             # Configuration settings

- Python 3.8+ (developed with Python 3.13)│
├── __init__.py             # Package initialization

- Google Gemini API key│
└── data/                   # Data storage directories

│       ├── raw/                # Raw uploaded files

### 1. Clone and Navigate│
├── processed/          # Processed document chunks


├── uploaded/           # Session-based uploads

git clone <repository-url>│
└── index/              # Vector indices

cd Assignment
├── tester.html                 # Web-based testing interface

├── requirements.txt            # Python dependencies

├── .env.example                # Environment configuration template

### 2. Install Dependencies
├── .gitignore                  # Git exclusions

└── README.md                   # This documentation

pip install -r requirements.txt```

```

## 🔧 Installation & Setup

### 3. Environment Configuration

Create or update `.env` file:### Prerequisites

```env- Python 3.8+ (developed with Python 3.13)

APP_NAME="Knowledge RAG API"- Google Gemini API key

APP_ENV=dev

HOST=0.0.0.0### 1. Clone and Navigate

PORT=8000```bash

GOOGLE_API_KEY=your_gemini_api_key_heregit clone <repository-url>

GEMINI_MODEL=models/gemini-2.0-flashcd Assignment

``````



### 4. Start the Server### 2. Install Dependencies

```bash```bash

uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reloadpip install -r requirements.txt

``````



The API will be available at `http://localhost:8000`### 3. Environment Configuration

Create or update `.env` file:

## Usage```env

APP_NAME="Knowledge RAG API"

### Web Interface (Recommended for Testing)APP_ENV=dev

1. Open `tester.html` in your browserHOST=0.0.0.0

2. Upload a PDF or TXT filePORT=8000

3. Ask questions about the document contentGOOGLE_API_KEY=your_gemini_api_key_here

4. Get grounded, cited responsesGEMINI_MODEL=models/gemini-2.0-flash

```

### API Endpoints

### 4. Start the Server

#### Health Check```bash

```bashuvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload

GET /healthz```

```

The API will be available at `http://localhost:8000`

#### Upload Document

```bash## Usage

POST /upload

Content-Type: multipart/form-data### Web Interface (Recommended for Testing)

File: document.pdf or document.txt1. Open `tester.html` in your browser

```2. Upload a PDF or TXT file

3. Ask questions about the document content

Response:4. Get grounded, cited responses

```json

{### API Endpoints

  "session_id": "unique-session-id",

  "message": "Document uploaded and indexed successfully",#### Health Check

  "chunks": 15,```bash

  "filename": "document.pdf"GET /healthz

}```

```

#### Upload Document

#### Ask Question```bash

```bashPOST /upload

POST /askContent-Type: multipart/form-data

Content-Type: application/jsonFile: document.pdf or document.txt

```

{

  "session_id": "unique-session-id",Response:

  "q": "What is the refund policy?",```json

  "k": 6,{

  "strict": true  "session_id": "unique-session-id",

}  "message": "Document uploaded and indexed successfully",

```  "chunks": 15,

  "filename": "document.pdf"

Response:}

```json```

{

  "answer": "The company offers a 30-day return policy for all products [1]. Customers must provide a receipt for all returns [1].",#### Ask Question

  "session_id": "unique-session-id",```bash

  "question": "What is the refund policy?",POST /ask

  "retrieved_blocks": ["Block content with citations..."],Content-Type: application/json

  "method": "tfidf_gemini"

}{

```  "session_id": "unique-session-id",

  "q": "What is the refund policy?",

#### Debug Models (Development)  "k": 6,

```bash  "strict": true

GET /debug/models}

``````



### Query ExamplesResponse:

```json

#### Specific Questions{

- "What is the refund policy?"  "answer": "The company offers a 30-day return policy for all products [1]. Customers must provide a receipt for all returns [1].",

- "How do I reset my password?"  "session_id": "unique-session-id",

- "What are the business hours?"  "question": "What is the refund policy?",

  "retrieved_blocks": ["Block content with citations..."],

#### Summary Questions  "method": "tfidf_gemini"

- "Provide a summary of the whole document"}

- "What does this document contain?"```

- "Give me an overview of the main topics"

#### Debug Models (Development)

#### Short/Fuzzy Queries```bash

- "refund" → Enhanced to "refund policy return"GET /debug/models

- "pasword" → Corrected to "password"```

- "hrs" → Expanded to "hours business"

### Query Examples

## Testing

#### Specific Questions

### Testing the System- "What is the refund policy?"

- "How do I reset my password?"

#### Web Interface Testing (Recommended)- "What are the business hours?"

1. Open `tester.html` in your browser

2. Upload a PDF or TXT document#### Summary Questions

3. Test various question types:- "Provide a summary of the whole document"

   - **Document Content**: "What does this document contain?"- "What does this document contain?"

   - **Summaries**: "Provide a summary of the document"- "Give me an overview of the main topics"

   - **Specific Questions**: "What is the refund policy?"

   - **Main Topics**: "What are the key points?"#### Short/Fuzzy Queries

- "refund" → Enhanced to "refund policy return"

#### API Testing- "pasword" → Corrected to "password"

Use curl or any HTTP client to test the endpoints:- "hrs" → Expanded to "hours business"



```bash##  Testing

# Upload a document

curl -X POST "http://localhost:8000/upload" -F "file=@your_document.pdf"### Testing the System



# Ask questions (use session_id from upload response)#### Web Interface Testing (Recommended)

curl -X POST "http://localhost:8000/ask" \1. Open `tester.html` in your browser

  -H "Content-Type: application/json" \2. Upload a PDF or TXT document

  -d '{"session_id":"your-session-id","q":"What does this document contain?","strict":true}'3. Test various question types:

```   - **Document Content**: "What does this document contain?"

   - **Summaries**: "Provide a summary of the document"

## Architecture   - **Specific Questions**: "What is the refund policy?"

   - **Main Topics**: "What are the key points?"

### RAG Pipeline

1. **Document Processing**: #### API Testing

   - PDF/TXT extraction using pypdfUse curl or any HTTP client to test the endpoints:

   - Text chunking with overlap for context preservation

   - TF-IDF vectorization with n-gram support (1-3 words)```bash

# Upload a document

2. **Query Processing**:curl -X POST "http://localhost:8000/upload" -F "file=@your_document.pdf"

   - Fuzzy correction for typos using difflib

   - Synonym expansion for short queries# Ask questions (use session_id from upload response)

   - Dynamic parameter adjustment based on query lengthcurl -X POST "http://localhost:8000/ask" \

  -H "Content-Type: application/json" \

3. **Retrieval & Generation**:  -d '{"session_id":"your-session-id","q":"What does this document contain?","strict":true}'

   - TF-IDF cosine similarity for relevant chunk retrieval```

   - Google Gemini AI for natural language generation

   - Strict grounding validation with citation requirements## Architecture

   - Fallback to "I don't know" for out-of-scope queries

### RAG Pipeline

### Key Components1. **Document Processing**: 

   - PDF/TXT extraction using pypdf

#### `backend/app.py` - Main Application   - Text chunking with overlap for context preservation

- FastAPI server with CORS support   - TF-IDF vectorization with n-gram support (1-3 words)

- Session-based document management

- Dual RAG implementation (TF-IDF + FAISS)2. **Query Processing**:

- Gemini integration with strict grounding   - Fuzzy correction for typos using difflib

- Enhanced query processing (fuzzy, n-gram, synonyms)   - Synonym expansion for short queries

   - Dynamic parameter adjustment based on query length

#### `backend/rag_pipeline.py` - Multi-Document RAG

- FAISS vector store integration3. **Retrieval & Generation**:

- Sentence transformer embeddings   - TF-IDF cosine similarity for relevant chunk retrieval

- Advanced retrieval and reranking   - Google Gemini AI for natural language generation

   - Strict grounding validation with citation requirements

#### Smart Query Enhancement   - Fallback to "I don't know" for out-of-scope queries

- **Fuzzy Correction**: Automatic typo detection and correction

- **N-gram Processing**: 1-3 word phrase matching for better relevance### Key Components

- **Synonym Expansion**: Enriches short queries with related terms

- **Dynamic Parameters**: Adjusts TF-IDF settings based on query characteristics#### `backend/app.py` - Main Application

- FastAPI server with CORS support

## Security & Configuration- Session-based document management

- Dual RAG implementation (TF-IDF + FAISS)

### Environment Variables- Gemini integration with strict grounding

- `GOOGLE_API_KEY`: Required for Gemini AI integration- Enhanced query processing (fuzzy, n-gram, synonyms)

- `GEMINI_MODEL`: Specify model version (default: models/gemini-2.0-flash)

- `HOST`/`PORT`: Server configuration#### `backend/rag_pipeline.py` - Multi-Document RAG

- FAISS vector store integration

### Data Privacy- Sentence transformer embeddings

- Session-based isolation prevents cross-document leakage- Advanced retrieval and reranking

- Temporary storage with configurable cleanup

- No persistent storage of sensitive content#### Smart Query Enhancement

- **Fuzzy Correction**: Automatic typo detection and correction

## Production Considerations- **N-gram Processing**: 1-3 word phrase matching for better relevance

- **Synonym Expansion**: Enriches short queries with related terms

### Scaling- **Dynamic Parameters**: Adjusts TF-IDF settings based on query characteristics

- Consider Redis for session management in multi-instance deployments

- Implement proper rate limiting for API endpoints## Security & Configuration

- Add authentication and authorization layers

### Environment Variables

### Monitoring- `GOOGLE_API_KEY`: Required for Gemini AI integration

- Built-in health checks at `/healthz`- `GEMINI_MODEL`: Specify model version (default: models/gemini-2.0-flash)

- Debug endpoints for development (`/debug/models`)- `HOST`/`PORT`: Server configuration

- Comprehensive error handling with fallbacks

### Data Privacy

### Performance- Session-based isolation prevents cross-document leakage

- Efficient TF-IDF caching per session- Temporary storage with configurable cleanup

- Optimized chunk retrieval with configurable top-k- No persistent storage of sensitive content

- Streaming responses for large documents (future enhancement)

## Production Considerations

## Contributing

### Scaling

1. Fork the repository- Consider Redis for session management in multi-instance deployments

2. Create a feature branch- Implement proper rate limiting for API endpoints

3. Add comprehensive tests for new features- Add authentication and authorization layers

4. Ensure all existing tests pass

5. Submit a pull request### Monitoring

- Built-in health checks at `/healthz`

## License- Debug endpoints for development (`/debug/models`)

- Comprehensive error handling with fallbacks

This project is licensed under the MIT License - see the LICENSE file for details.

### Performance

## Acknowledgments- Efficient TF-IDF caching per session

- Optimized chunk retrieval with configurable top-k

- Built with FastAPI for high-performance API development- Streaming responses for large documents (future enhancement)

- Powered by Google Gemini AI for natural language generation

- Uses scikit-learn for efficient text processing## Contributing

- Enhanced with sentence-transformers for semantic search

1. Fork the repository

---2. Create a feature branch

3. Add comprehensive tests for new features

**Ready to get started?** Upload a document via `tester.html` and ask your first question!4. Ensure all existing tests pass
5. Submit a pull request



## Acknowledgments

- Built with FastAPI for high-performance API development
- Powered by Google Gemini AI for natural language generation
- Uses scikit-learn for efficient text processing
- Enhanced with sentence-transformers for semantic search

---

**Ready to get started?** Upload a document via `tester.html` and ask your first question! 🚀
