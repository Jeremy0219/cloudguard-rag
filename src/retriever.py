"""
retriever.py
Handles vector search against Azure AI Search to retrieve relevant document chunks.
"""

import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential

load_dotenv()

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY")),
)

TOP_K = 5  # number of chunks to retrieve


def retrieve(query_embedding: list[float]) -> list[dict]:
    """
    Run a vector search against Azure AI Search.
    Returns the top-K most relevant chunks.
    """
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=TOP_K,
        fields="embedding",
    )

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=["id", "source", "content"],
    )

    chunks = []
    for result in results:
        chunks.append({
            "id": result["id"],
            "source": result["source"],
            "content": result["content"],
        })

    return chunks