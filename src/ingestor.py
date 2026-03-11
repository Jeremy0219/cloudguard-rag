"""
ingestor.py
Handles document loading, chunking, embedding, and indexing into Azure AI Search.
"""

import os
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
from azure.core.credentials import AzureKeyCredential
from rich.console import Console
from rich.progress import track

load_dotenv()

console = Console()

# Embedding model runs locally
embedder = SentenceTransformer("all-MiniLM-L6-v2")
VECTOR_DIM = 384  # dimension for all-MiniLM-L6-v2

# Azure AI Search clients
search_credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
index_client = SearchIndexClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    credential=search_credential,
)
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=search_credential,
)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_pdf(filepath: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_text(text: str, source: str) -> list[dict]:
    """Split text into overlapping chunks."""
    # Sanitize source name for use as Azure Search key
    safe_source = source.replace(".", "-").replace(" ", "_")
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({
                "id": f"{safe_source}_{chunk_id}",
                "source": source,
                "content": chunk,
            })
            chunk_id += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a given text string."""
    return embedder.encode(text).tolist()


def create_index():
    """Create the Azure AI Search index with vector search support."""
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=VECTOR_DIM,
            vector_search_profile_name="myHnswProfile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
        profiles=[VectorSearchProfile(name="myHnswProfile", algorithm_configuration_name="myHnsw")],
    )

    index = SearchIndex(
        name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
        fields=fields,
        vector_search=vector_search,
    )

    index_client.create_or_update_index(index)
    console.print("[bold green]✓ Azure AI Search index created/updated[/bold green]")


def ingest_documents(docs_folder: str):
    """Main ingestion pipeline: load → chunk → embed → index."""
    create_index()

    docs_path = os.listdir(docs_folder)
    all_chunks = []

    for filename in docs_path:
        if filename.endswith(".pdf"):
            filepath = os.path.join(docs_folder, filename)
            source = filename.replace(".pdf", "")
            console.print(f"[cyan]Loading:[/cyan] {filename}")
            text = load_pdf(filepath)
            chunks = chunk_text(text, source)
            console.print(f"  → {len(chunks)} chunks created")
            all_chunks.extend(chunks)

    if not all_chunks:
        console.print("[red]No PDF files found in docs folder.[/red]")
        return

    console.print(f"\n[bold]Embedding and indexing {len(all_chunks)} chunks...[/bold]")

    documents = []
    for chunk in track(all_chunks, description="Embedding..."):
        chunk["embedding"] = embed_text(chunk["content"])
        documents.append(chunk)

    # Upload in batches of 100
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        search_client.upload_documents(documents=batch)

    console.print(f"\n[bold green]✓ Successfully indexed {len(documents)} chunks into Azure AI Search![/bold green]")