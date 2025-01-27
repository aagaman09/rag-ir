
# RAG Application with Gemini and ChromaDB

```bash
rag-ir/
├── main.py
├── rag/
│   ├── __init__.py
│   ├── db.py
│   ├── document_loader.py
│   └── llm.py
├── requirements.txt
└── README.md
```

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

