# Loan-Assistance
A lightweight RAG chatbot that answers user queries about Bank of Maharashtra’s loan products. It leverages scraped official loan data, semantic search with FAISS, and OpenAI’s GPT-3.5-turbo (ChatGPT) to provide accurate, context-aware responses. Includes data scraping, processing, vector search, and LLM integration with a modular Python codebase.

**Loan Product Assistant – Bank of Maharashtra
Project Overview**
This project is a Loan Product Assistant designed to answer questions specifically about Bank of Maharashtra’s loan products. It implements a lightweight Retrieval-Augmented Generation (RAG) pipeline that retrieves relevant loan data from a structured knowledge base and generates natural language answers using advanced AI models.

Project Setup
Clone the repository:

**git clone <your-repo-url>**

Install dependencies:

**pip install -r requirements.txt**

Environment variables:

In .env file in the project root directory and add the following variables:

Your OpenAI API key for accessing the GPT models
OPENAI_API_KEY=your_openai_api_key_here

Important:
Replace your_openai_api_key_here with your actual OpenAI API key. You can get this key from your OpenAI account dashboard under the API section. Paste it exactly as it is here to enable API access.

**Why encode the system prompt?**

The system prompt is base64 encoded to:

Prevent accidental editing or formatting issues in environment files

Keep the prompt secure and less exposed in plain text

Ensure proper decoding at runtime for sending to the LLM

Run the application:

**python main.py**
The application will prompt you to enter your loan-related questions and return answers based on Bank of Maharashtra’s loan data.

Architectural Decisions
**Libraries**
Scraping & Data Processing:

Used Python's requests and BeautifulSoup for scraping official Bank of Maharashtra loan product pages. These libraries are effective for static HTML content extraction.

RAG Pipeline & Embeddings:
Used sentence-transformers with the all-MiniLM-L6-v2 model for embedding textual data and queries, offering a balance between accuracy and speed.

Vector Store:
Employed FAISS for fast, in-memory similarity search, avoiding the overhead of complex vector databases.


**Data Strategy**
Extracted and cleaned loan data into key fields for a focused knowledge base.

Chunked loan descriptions into overlapping 500-character segments using RecursiveCharacterTextSplitter for precise retrieval.

Embedded chunks with SentenceTransformers and indexed with FAISS for efficient semantic search.



**Model Selection**
Embedding Model: all-MiniLM-L6-v2 for effective semantic similarity.

LLM: OpenAI GPT-3.5-turbo for reliable, controlled natural language generation.

**AI Tools Used**
Mistral: For frontend AI inference.

Grok AI: For logic processing within the assistant.

OpenAI GPT-3.5-turbo: For answer generation.

Sentence-Transformers & FAISS: For embedding and vector search.

**Challenges Faced**
Handling dynamic content loading on Bank of Maharashtra pages required additional techniques.

Data normalization was necessary due to inconsistent formatting across scraped pages.

Crafting the system prompt to ensure the assistant clearly identifies itself and accurately explains loan details.


**Potential Improvements**
Integrate real-time APIs for live loan data updates.

Enhance retrieval with hybrid search or reranking for better accuracy.

Fine-tune models on Bank of Maharashtra-specific corpora.

Develop a polished, multilingual frontend with a conversational UI.

Add robust error handling and fallback responses.

