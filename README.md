<<<<<<< HEAD
# rag-ir
=======
# RAG Application with Phi3 Model and ChromaDB

Welcome to the RAG (Retrieval-Augmented Generation) application repository! This project leverages the Gemini model and ChromaDB to read PDF documents, embed their content, store the embeddings in a database, and perform retrieval-augmented generation.



## Introduction

This repository contains a RAG application that reads PDF files, generates embeddings using the Alibaba-NLP/gte-large-en-v1.5 model, stores these embeddings in ChromaDB, and performs retrieval-augmented generation to provide contextual answers based on the embedded content. The system is designed to enhance the capability of answering queries by leveraging the context from the embedded documents.

## Features

- **PDF Reading**: Extracts text content from PDF documents.
- **Embedding Generation**: Utilizes the Alibaba-NLP/gte-large-en-v1.5 model to generate embeddings for the extracted text.
- **Database Storage**: Stores the generated embeddings in ChromaDB.
- **Retrieval-Augmented Generation**: Retrieves relevant embeddings from the database and generates contextually accurate responses.

## Installation

**Note:** On first installation, this script will download the necessary NLTK stopwords, the NLP embedding model, and the large language model (LLM). As a result, the initial execution may take longer than subsequent runs.

To get started with the RAG application, follow these steps:


1. **Clone the repository**:

    ```bash
    git clone https://github.com/aagaman09/rag-ir.git
    cd rag-ir
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv/Scripts/activate`
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Run the script

```bash
streamlit run main.py
```

