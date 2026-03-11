"""
main.py
CloudGuard RAG Assistant — interactive CLI entrypoint.
"""

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from src.ingestor import embed_text
from src.retriever import retrieve
from src.generator import generate_answer

console = Console()


def run():
    console.print(Panel(
        Text("🔐 CloudGuard RAG Assistant", justify="center", style="bold cyan"),
        subtitle="Powered by Claude AI + Azure AI Search",
        border_style="cyan",
    ))
    console.print("[dim]Ask questions about cloud security frameworks. Type 'exit' to quit.[/dim]\n")

    while True:
        query = Prompt.ask("[bold green]You[/bold green]")

        if query.lower() in ("exit", "quit"):
            console.print("[dim]Goodbye.[/dim]")
            break

        if not query.strip():
            continue

        with console.status("[bold cyan]Searching security frameworks...[/bold cyan]"):
            # Step 1: Embed the query
            query_embedding = embed_text(query)

            # Step 2: Retrieve relevant chunks from Azure AI Search
            chunks = retrieve(query_embedding)

        if not chunks:
            console.print("[red]No relevant content found. Try rephrasing your question.[/red]\n")
            continue

        with console.status("[bold cyan]Generating answer...[/bold cyan]"):
            # Step 3: Generate grounded answer with Claude
            answer = generate_answer(query, chunks)

        console.print(f"\n[bold cyan]CloudGuard:[/bold cyan]")
        console.print(Markdown(answer))
        console.print()


if __name__ == "__main__":
    run()