"""
generator.py
Uses Anthropic Claude to generate grounded answers from retrieved context chunks.
"""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are CloudGuard, an expert cloud security assistant.
Answer questions strictly based on the provided context from cloud security frameworks.
Always cite the source document for each key point in your answer.
Format your response clearly with the answer first, followed by a "Sources:" section.
If the context does not contain enough information to answer, say so clearly.
Do not use any knowledge outside of the provided context.
"""


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    """
    Generate a grounded answer using Claude given a query and retrieved chunks.
    """
    # Build context string from retrieved chunks
    context = ""
    for i, chunk in enumerate(context_chunks):
        context += f"\n[Source {i+1}: {chunk['source']}]\n{chunk['content']}\n"

    # Build the user message
    user_message = f"""Use the following context from cloud security frameworks to answer the question.

CONTEXT:
{context}

QUESTION:
{query}
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ],
    )

    return response.content[0].text