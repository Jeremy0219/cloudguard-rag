"""
ingest.py
Entrypoint for ingesting security framework documents into Azure AI Search.

Usage:
    python ingest.py --docs ./docs/
"""

import argparse
from rich.console import Console
from src.ingestor import ingest_documents

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into CloudGuard index.")
    parser.add_argument("--docs", type=str, default="./docs/", help="Path to documents folder")
    args = parser.parse_args()

    console.print(f"\n[bold cyan]CloudGuard Ingestion Pipeline[/bold cyan]")
    console.print(f"[dim]Documents folder: {args.docs}[/dim]\n")

    ingest_documents(args.docs)


if __name__ == "__main__":
    main()