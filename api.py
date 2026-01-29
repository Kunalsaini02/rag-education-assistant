import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -----------------------------
# Clients
# -----------------------------
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

groq_client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="RAG Education Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request model
# -----------------------------
class QueryRequest(BaseModel):
    query: str

# -----------------------------
# API endpoint
# -----------------------------
@app.post("/ask")
def ask_question(req: QueryRequest):
    try:
        query = req.query.strip()
        if not query:
            return {"answer": "Please ask a valid question."}

        # 🔍 Azure AI Search
        results = search_client.search(
            search_text=query,
            select=["content"],
            top=3
        )

        documents = list(results)
        if not documents:
            return {
                "answer": "I couldn't find relevant information in the notes."
            }

        context_parts = [
            doc["content"] for doc in documents if doc.get("content")
        ]

        if not context_parts:
            return {
                "answer": "Relevant documents were found, but no readable content."
            }

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an educational assistant.
Answer ONLY using the context below.
If the answer is not present, say "I don't know based on the given material."

Context:
{context}

Question:
{query}

Answer:
"""

        # 🤖 Groq LLM (UNCHANGED MODEL)
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content.strip()

        return {"answer": answer}

    except Exception as e:
        return {
            "answer": "Something went wrong on the server.",
            "error": str(e)
        }


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "RAG Education Assistant",
        "message": "Backend is running successfully"
    }