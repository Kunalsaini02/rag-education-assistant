from groq import Groq
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def build_context(docs):
    context_parts = []

    for i, doc in enumerate(docs, start=1):
        text = doc.get("content", "")
        source = doc.get("source", "unknown")

        chunk = f"[Source {i}: {source}]\n{text}"
        context_parts.append(chunk)

    return "\n\n".join(context_parts)


# -------------------------
# AZURE AI SEARCH
# -------------------------
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

print("🔍 Searching documents...\n")

# query = "Compare deadlock prevention vs avoidance"
query = "Explain ostrich algorithm drawbacks"

results = search_client.search(
    search_text=query,
    search_fields=["content"],
    select=["content", "source"],
    top=3
)

documents = list(results)

for i, doc in enumerate(documents, start=1):
    print(f"\n📄 Document {i}")
    print("Source:", doc.get("source"))
    print("Content:", doc.get("content", "")[:500])


# -------------------------
# BUILD CONTEXT
# -------------------------
context = build_context(documents)

print("\n================ CONTEXT ================\n")
print(context)
print("\n=========================================\n")


# -------------------------
# RAG MESSAGES (FIXED)
# -------------------------
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful educational assistant. "
            "Answer strictly using the provided context. "
            "If the answer is not present in the context, say "
            "'I don't know based on the given material.'"
        )
    },
    {
        "role": "user",
        "content": f"""
Context:
{context}

Question:
{query}
"""
    }
]


# -------------------------
# GROQ LLM
# -------------------------
groq_client = Groq(api_key=GROQ_API_KEY)

response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages,
    temperature=0.2
)


answer = response.choices[0].message.content


print("\n================ FINAL ANSWER ================\n")
print(answer)
print("\n=============================================\n")
