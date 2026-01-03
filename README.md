# VibeVerifier

<div align="center">

**Universal AI Hallucination & Citation Verification System**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/kshitijmarwah1/VibeCoders-AI-Citation-System)

A generic, domain-aware, multi-input AI verification system designed to detect hallucinations, verify factual claims using real web sources, and provide explainable, human-readable reasoning.

[Documentation](#documentation) • [Installation](#installation) • [Features](#features) • [API Reference](#api-reference) • [Contributing](#contributing)

</div>

## 🎬 Presentation & Demo

- **📊 Project Presentation**: [Add PPT/Slides Link Here]
- **🎥 Demo Video**: [Add Demo Video Link Here]
- **🌐 Live Demo**: [Add Live Demo URL Here (if available)]

---

---

## 📋 Table of Contents

- [Overview](#overview)
- [Presentation & Demo](#presentation--demo)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Design Principles](#design-principles)
- [Contributing](#contributing)
- [License](#license)
- [Collaborators](#collaborators)

---

## 🎯 Overview

**VibeVerifier** is a universal verification engine that analyzes and verifies factual claims in any content. Unlike traditional fact-checking tools, VibeVerifier is designed to work across multiple domains (medical, finance, legal, technology, general) and supports various input formats (text, URLs, PDFs, DOCX files).

### What is VibeVerifier?

VibeVerifier is an AI-powered system that:

- **Detects Hallucinations**: Identifies false or unverified claims in AI-generated or human-written content
- **Verifies Claims**: Uses real-time web search to verify factual claims against authoritative sources
- **Provides Confidence Scores**: Assigns reliability scores based on multiple factors (similarity, credibility, contradictions)
- **Offers Explainability**: Generates human-readable explanations for verification decisions
- **Works Across Domains**: Adapts verification criteria based on content domain
- **Supports Multiple Inputs**: Processes text, URLs, PDFs, and DOCX files seamlessly

### Key Differentiators

- **Universal**: Works for any user, any domain, any input format
- **Open Source Models Only**: Uses only pretrained, free, open-source models
- **Multi-User Safe**: No per-user customization, deterministic verification
- **Real-Time Verification**: Leverages web search for up-to-date information
- **Explainable AI**: Provides clear reasoning for every verification decision

---

## 🎬 Presentation & Demo

- **📊 Project Presentation**: [Add PPT/Slides Link Here]
- **🎥 Demo Video**: [Add Demo Video Link Here]
- **🌐 Live Demo**: [Add Live Demo URL Here (if available)]

---

## ✨ Features

### Core Features

#### 1. **Multi-Format Input Support**
   - **Text Input**: Direct text input for quick verification
   - **URL Input**: Fetch and verify content from web pages
   - **File Upload**: Support for PDF and DOCX documents
   - **Batch Processing**: Verify multiple URLs or combined text and URLs

#### 2. **Domain-Aware Verification**
   - **Automatic Domain Detection**: Identifies content domain (medical, finance, legal, technology, general)
   - **Domain-Specific Thresholds**: Adjusts verification criteria based on domain
   - **Credibility Weighting**: Different source credibility scores per domain
   - **Specialized Handling**: Optimized verification for domain-specific content

#### 3. **Real-Time Progress Tracking**
   - **Dynamic Progress Bars**: Real-time progress updates during verification
   - **Batch-Level Tracking**: Progress tracked by batch completion for efficient processing
   - **Granular Updates**: Detailed progress information for text inputs
   - **Server-Sent Events (SSE)**: Real-time progress streaming

#### 4. **Comprehensive Verification Results**
   - **Claim Extraction**: Automatically identifies factual claims from content
   - **Verification Status**: Categorizes claims as verified, hallucinated, unverified, or error
   - **Confidence Scores**: Multi-factor scoring system (confidence, similarity, credibility)
   - **Citation Links**: Provides source URLs with relevant snippets
   - **Contradiction Detection**: Identifies conflicting information across sources
   - **Human-Readable Explanations**: LLM-generated explanations for verification decisions

#### 5. **Advanced Scoring System**
   - **Similarity Scoring**: Semantic similarity between claims and sources
   - **Credibility Scoring**: Source reliability based on domain-specific criteria
   - **Contradiction Analysis**: Detects and flags contradictory sources
   - **Overall Reliability**: Aggregated score for the entire content

#### 6. **Citation Verification**
   - **URL Validation**: Verifies that citation URLs are accessible
   - **Citation Extraction**: Automatically extracts citations from content
   - **Verification Status**: Categorizes citations as verified or invalid

#### 7. **Modern Web Interface**
   - **Dark Theme UI**: Beautiful dark interface with neon accents (cyan, pink, purple)
   - **Animated Gradient Background**: Soothing visual experience
   - **Responsive Design**: Works seamlessly on desktop and mobile devices
   - **Interactive Results Display**: Detailed claim analysis with expandable sections
   - **Drag & Drop File Upload**: Intuitive file upload interface

---

## 🏗️ Architecture

### System Overview

VibeVerifier follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐
│   Frontend      │  Next.js + React + TypeScript
│   (Web UI)      │
└────────┬────────┘
         │
         │ HTTP/REST API
         │
┌────────▼──────────────────────────────────────────┐
│            Backend API (FastAPI)                  │
│  ┌────────────────────────────────────────────┐  │
│  │  Input Processing Layer                    │  │
│  │  - Text normalization                      │  │
│  │  - PDF/DOCX extraction                     │  │
│  │  - URL content fetching                    │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │  Claim Processing Layer                    │  │
│  │  - Sentence segmentation                   │  │
│  │  - Claim extraction                        │  │
│  │  - Domain detection                        │  │
│  │  - Sentiment analysis                      │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │  Verification Engine                       │  │
│  │  - Web search (Tavily API)                 │  │
│  │  - Semantic similarity                     │  │
│  │  - Credibility scoring                     │  │
│  │  - Contradiction detection                 │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │  Scoring & Explanation                     │  │
│  │  - Multi-factor scoring                    │  │
│  │  - LLM reasoning (explanations)            │  │
│  │  - Citation verification                   │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Data Flow

1. **Input Reception**: User submits content (text/URL/file)
2. **Normalization**: Content is normalized to plain text
3. **Claim Extraction**: Sentences are segmented and factual claims are extracted
4. **Domain Detection**: System identifies the content domain
5. **Verification**: Each claim is verified against web sources
6. **Scoring**: Claims are scored based on similarity, credibility, and contradictions
7. **Explanation**: LLM generates human-readable explanations
8. **Results**: Comprehensive results are returned to the user

### Key Components

- **Input Processing**: Handles multiple input formats and normalizes them
- **Claim Extraction**: Intelligent sentence segmentation and claim identification
- **Domain Classifier**: Detects content domain for specialized verification
- **Web Search Integration**: Tavily API for real-time source retrieval
- **Semantic Similarity**: Sentence transformers for claim-source matching
- **Credibility Engine**: Domain-aware source credibility assessment
- **Contradiction Detector**: Identifies conflicting information
- **LLM Reasoner**: Generates explanations (advisory only, never determines truth)
- **Citation Verifier**: Validates citation URLs

---

## 📦 Installation

### Prerequisites

- **Python**: 3.9 or higher
- **Node.js**: 18.0 or higher
- **npm/yarn/pnpm**: Latest stable version
- **Tavily API Key**: [Get one here](https://tavily.com)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 2GB free space

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kshitijmarwah1/VibeCoders-AI-Citation-System.git
   cd VibeCoders-AI-Citation-System
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the `backend` directory:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

4. **Start the backend server**
   ```bash
   uvicorn services.api.main:app --reload --port 8000
   ```

5. **Set up the frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   
   # Optional: Create .env.local to customize API URL
   echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local
   ```

6. **Start the frontend development server**
   ```bash
   npm run dev
   ```

7. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000)

For detailed installation instructions, see the [Documentation](#documentation) section.

---

## ⚙️ Configuration

### Backend Configuration

Create a `.env` file in the `backend` directory:

```env
# Required: Tavily API Key for web search
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: Custom port (default: 8000)
PORT=8000

# Optional: Logging level (default: INFO)
LOG_LEVEL=INFO
```

### Frontend Configuration

Create a `.env.local` file in the `frontend` directory (optional):

```env
# Backend API URL (default: http://127.0.0.1:8000)
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### Domain Configuration

Domain-specific settings can be customized in `backend/services/config/domains/`:

- `general.yaml` - General purpose verification
- `medical.yaml` - Medical/healthcare domain
- `finance.yaml` - Financial domain
- `legal.yaml` - Legal domain
- `technology.yaml` - Technology domain

Edit these YAML files to adjust credibility scores, similarity thresholds, and domain-specific keywords.

---

## 🚀 Usage

### Web Interface

1. Navigate to the web interface (default: http://localhost:3000)
2. Choose input type (Text, URL, or File)
3. Enter or upload your content
4. Click "Verify" and watch the progress bar
5. Review the verification results with confidence scores and citations

### API Usage

#### Verify Text
```bash
curl -X POST "http://localhost:8000/verify/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth orbits the Sun."}'
```

#### Verify URL
```bash
curl -X POST "http://localhost:8000/verify/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

#### Verify File
```bash
curl -X POST "http://localhost:8000/verify/file" \
  -F "file=@document.pdf"
```

#### Check Progress
```bash
curl "http://localhost:8000/progress/{task_id}"
```

For detailed API documentation, see the [API Reference](#api-reference) section.

---

## 📚 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/verify/text` | Verify text content |
| POST | `/verify/url` | Verify content from URL |
| POST | `/verify/file` | Verify uploaded file (PDF/DOCX) |
| POST | `/verify/batch` | Verify batch input (text and/or URLs) |
| GET | `/progress/{task_id}` | Get progress status |
| GET | `/progress/stream/{task_id}` | Stream progress (SSE) |
| GET | `/health` | Health check endpoint |
| GET | `/docs` | Interactive API documentation (Swagger UI) |

### Response Format

```json
{
  "task_id": "uuid-string",
  "domain": "general",
  "total_claims": 3,
  "overall_reliability": 0.85,
  "claims": [
    {
      "claim": "The claim text",
      "status": "verified",
      "confidence": 0.92,
      "similarity": 0.88,
      "credibility": 0.90,
      "contradicted": false,
      "citations": [
        {
          "url": "https://example.com/source",
          "title": "Source Title",
          "snippet": "Relevant snippet..."
        }
      ],
      "explanation": "Human-readable explanation..."
    }
  ],
  "extracted_citations": {},
  "citation_verification": {
    "verified": [],
    "invalid": [],
    "total": 0
  }
}
```

### Interactive Documentation

When the backend is running, interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📖 Documentation

Comprehensive documentation is available in the web interface. When running the application locally, access it at:

- **Web Interface Docs**: [http://localhost:3000/docs](http://localhost:3000/docs) (when frontend is running)
- **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs) (when backend is running)
- **API Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc) (when backend is running)

The documentation includes:

- **Setup Guide**: Detailed installation and configuration instructions
- **API Documentation**: Complete API reference with examples
- **Architecture**: System design and component details
- **Privacy Policy**: Data handling and privacy information
- **Contributing Guide**: How to contribute to the project

Access the documentation by clicking the "Docs" button in the navigation bar of the web interface, or visit the URLs above when the servers are running.

---

## 📁 Project Structure

```
VibeCoders-AI-Citation-System/
├── backend/                          # Python FastAPI backend
│   ├── services/
│   │   ├── api/                     # API routes and endpoints
│   │   │   ├── main.py             # FastAPI application
│   │   │   └── routers/
│   │   │       ├── verify.py       # Verification endpoints
│   │   │       └── progress.py     # Progress tracking
│   │   ├── core/                   # Core verification logic
│   │   │   ├── claims/            # Claim extraction
│   │   │   │   ├── extractor.py
│   │   │   │   ├── domain_detector.py
│   │   │   │   ├── sentence_segmenter.py
│   │   │   │   └── sentiment_analyzer.py
│   │   │   ├── verification/      # Verification engine
│   │   │   │   ├── verify.py
│   │   │   │   ├── verify_async.py
│   │   │   │   ├── search.py
│   │   │   │   └── citation_verifier.py
│   │   │   ├── scoring/           # Scoring algorithms
│   │   │   │   ├── aggregation.py
│   │   │   │   ├── credibility.py
│   │   │   │   └── domain.py
│   │   │   ├── llm/               # LLM integration
│   │   │   │   └── reasoner.py
│   │   │   ├── input/             # Input processing
│   │   │   │   ├── normalize.py
│   │   │   │   ├── text.py
│   │   │   │   ├── url.py
│   │   │   │   ├── pdf.py
│   │   │   │   └── docx.py
│   │   │   └── explainability/   # Explainability features
│   │   │       └── traces.py
│   │   ├── config/                # Configuration files
│   │   │   ├── settings.py
│   │   │   ├── domain_loader.py
│   │   │   └── domains/          # Domain-specific configs
│   │   │       ├── general.yaml
│   │   │       ├── medical.yaml
│   │   │       ├── finance.yaml
│   │   │       ├── legal.yaml
│   │   │       └── technology.yaml
│   │   └── storage/               # Storage utilities
│   │       └── cache.py
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment variables
├── frontend/                       # Next.js React frontend
│   ├── app/                       # Next.js app directory
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Home page
│   │   └── docs/                 # Documentation pages
│   │       └── page.tsx
│   ├── components/                # React components
│   │   ├── ui/                   # ShadCN UI components
│   │   ├── Navbar.tsx
│   │   ├── InputArea.tsx
│   │   ├── ResultsDisplay.tsx
│   │   ├── DynamicProgressBar.tsx
│   │   └── AnimatedGradient.tsx
│   ├── lib/                       # Utility functions
│   │   └── utils.ts
│   ├── package.json              # Node.js dependencies
│   └── .env.local                # Frontend environment variables
└── README.md                     # This file
```

---

## 🛠️ Technology Stack

### Backend

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server implementation
- **Pydantic** - Data validation using Python type annotations
- **Transformers** - Hugging Face transformers library for NLP
- **Sentence-Transformers** - Semantic similarity models
- **PyTorch** - Deep learning framework
- **scikit-learn** - Machine learning utilities
- **NLTK** - Natural Language Toolkit
- **Tavily API** - Web search and source retrieval
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX file processing
- **beautifulsoup4** - HTML parsing
- **sse-starlette** - Server-Sent Events support

### Frontend

- **Next.js 16** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS 4** - Utility-first CSS framework
- **ShadCN UI** - Component library
- **Radix UI** - Accessible UI primitives
- **Lucide React** - Icon library

### Models & APIs

- **Sentence Transformers** - For semantic similarity calculations
- **NLTK Data** - For text tokenization and processing
- **Tavily API** - For web search and source retrieval
- **Hugging Face Models** - Pre-trained models (run locally)

---

## 🎯 Design Principles

VibeVerifier is built on core design principles that ensure reliability and fairness:

### 1. Deterministic Core
- Verification decisions come from deterministic logic (similarity scores, credibility weighting, contradiction detection)
- LLMs are never used to determine truth, only for explanations

### 2. LLMs Are Advisory Only
- LLMs are used ONLY for:
  - Explanations and reasoning summaries
- They must NOT:
  - Override verification status
  - Modify confidence scores
  - Introduce new claims

### 3. Single Unified Verification Pipeline
- All inputs (text, PDF, URL, DOCX, batch) funnel into a unified pipeline:
  ```
  normalized_text → claim extraction → verification
  ```

### 4. Domain-Aware, Not User-Aware
- Domains influence thresholds and models
- Users do NOT influence logic or configuration
- Ensures consistent, fair verification for all users

### 5. Pretrained-Only Mode
- No training data
- No fine-tuning
- All models are loaded from Hugging Face or similar public sources

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Description of changes"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**

### Contribution Guidelines

- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass
- Write clear commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2026 Kshitij Marwah**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 👥 Collaborators

### Project Makers

This project was created and maintained by:

<div align="center">

#### 👑 Dhruv Gupta
**GitHub**: [@BeastBoom](https://github.com/BeastBoom)  
**Contributions**: 7 commits

#### 👑 Kshitij Marwah
**GitHub**: [@kshitijmarwah1](https://github.com/kshitijmarwah1)  
**Contributions**: 2 commits

</div>


---

<div align="center">

**VibeVerifier** - Universal AI Hallucination & Citation Verification System

Made with ❤️ by VibeCoders

[⭐ Star us on GitHub](https://github.com/kshitijmarwah1/VibeCoders-AI-Citation-System) • [📖 Documentation](#documentation) • [🐛 Report Bug](https://github.com/kshitijmarwah1/VibeCoders-AI-Citation-System/issues) • [💡 Request Feature](https://github.com/kshitijmarwah1/VibeCoders-AI-Citation-System/issues) • [📄 License](LICENSE)

</div>

