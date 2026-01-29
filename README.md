# RAG Education Assistant

## Overview
This project is a Retrieval-Augmented Generation (RAG) based educational assistant
that answers questions strictly from provided study notes.

## Architecture
User → React Frontend → FastAPI Backend  
→ Azure AI Search (document retrieval)  
→ Groq LLM (answer generation)

## Tech Stack
- React (Vite)
- FastAPI (Python)
- Azure AI Search
- Groq LLM (llama-3.1-8b-instant)

## Features
- Context-grounded answers
- No hallucinations
- Loading & timeout handling
- Clean UI

## How to Run
1. Start backend (`uvicorn api:app --reload`)
2. Start frontend (`npm run dev`)
3. Ask questions from notes
