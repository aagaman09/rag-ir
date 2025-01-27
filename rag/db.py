import chromadb
from chromadb.utils import embedding_functions

CHROMA_DATA_PATH = "chroma_data/"
EMBED_MODEL = "Alibaba-NLP/gte-large-en-v1.5"

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
print("Chroma DB connected")

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL, trust_remote_code=True
)
print("Embedding function loaded")


def get_db_collection(collection_name: str) -> chromadb.Collection:
    """
    Get or create a Chroma DB collection.

    :param collection_name: Name of the collection
    :return: Chroma DB collection
    """
    try:
        collection = client.get_collection(
            collection_name,
            embedding_function=embedding_func,
        )
    except ValueError as e:
        print(e)
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_func,
            metadata={"hnsw:space": "cosine"},
        )

    return collection


def add_to_collection(
    collection: chromadb.Collection, documents: list, ids: list, metadata: list
):
    """
    Add documents to the Chroma DB collection.

    :param collection: Chroma DB collection
    :param documents: List of document contents
    :param ids: List of document IDs
    :param metadata: List of metadata dictionaries
    """
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadata,
    )
    print("Documents loaded to DB")


def query_collection(collection: chromadb.Collection, query_text: str):
    """
    Query the Chroma DB collection for relevant documents.

    :param collection: Chroma DB collection
    :param query_text: Query text
    :return: Query results
    """
    try:
        query_results = collection.query(
            query_texts=[query_text],
            n_results=3,
        )
        return query_results

    except Exception as e:
        print(f"An error occurred while querying the collection: {e}")
        return None


def generate_context(query_result: dict):
    """
    Generate context from query results.

    :param query_result: Query results from Chroma DB
    :return: Combined context as a string
    """
    context = ""
    for doc in query_result["documents"]:
        for i in doc:
            context += i
    return context


def get_all_documents(collection: chromadb.Collection):
    """
    Retrieve all documents from the collection.

    :param collection: Chroma DB collection
    :return: List of all documents in the collection
    """
    try:
        # Fetch all documents
        results = collection.get()
        documents = results["documents"]
        return documents
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return None
    
def delete_collection(collection_name: str):
    """
    Delete a Chroma DB collection.

    :param collection_name: Name of the collection to delete
    """
    try:
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' deleted.")
    except Exception as e:
        print(f"Error deleting collection: {e}")
