# RAG Education Assistant 📘

A **production-ready Retrieval-Augmented Generation (RAG) application** that answers user questions strictly from curated study notes using **Azure AI Search** and a **Large Language Model (Groq)**.

This project ensures **grounded, syllabus-based answers** and avoids hallucinations by design.

---

## 🔍 Problem Statement

Students often rely on generic AI tools that generate answers without referencing their actual syllabus or study material.  
This leads to:
- Inaccurate explanations
- Hallucinated content
- Poor exam relevance

**This project solves that problem** by retrieving answers only from trusted, indexed notes before generating responses.

---

## 🚀 Solution Overview

The system follows a **Retrieval-Augmented Generation (RAG)** pipeline:

1. User asks a question
2. Relevant documents are retrieved using **Azure AI Search**
3. Retrieved content is provided as context to an LLM
4. The LLM generates an answer **strictly grounded in the retrieved content**

---

## 🧠 Architecture
- User -> React Frontend (Netlify) -> FastAPI Backend (Render) -> Azure AI Search (Document Retrieval) -> Groq LLM (Answer Generation) -> Answer returned to User
---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- CSS
- Deployed on **Netlify**

### Backend
- FastAPI (Python)
- Deployed on **Render**

### AI & Retrieval
- Azure AI Search
- Groq LLM (`llama-3.1-8b-instant`)

### Other Tools
- GitHub (version control)
- Environment-based configuration (`.env`)

---

## ✨ Key Features

- 🔎 **Retrieval-Augmented Generation (RAG)**
- 📚 Answers grounded in indexed study notes
- ❌ No hallucinations
- ⏳ Loading states & timeout handling
- ⚠️ Graceful error handling
- 🌐 Fully deployed (frontend + backend)
- 💼 Portfolio & interview ready

---

## 🧪 Example Questions

- What is deadlock in operating systems?
- Explain the conditions required for deadlock.
- What is mutual exclusion?
- Difference between deadlock and starvation.

---

## 🖥️ Live Demo

- **Frontend**: https://rag-education-assistant.netlify.app/
- **Backend API**: https://rag-education-assistant-backend.onrender.com

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/rag-education-assistant.git
cd rag-education-assistant
```
## Backend Setup 
- pip install -r requirements.txt
- uvicorn api:app --reload

## Frontend Setup
- cd frontend
- npm install
- npm run dev

### 📈 Future Enhancements

1. Document citations & sources
2. Chat history
3. User authentication
4. Upload PDFs dynamically
5. Advanced ranking & filtering
6. Streaming responses

### 👤 Author

Kunal Saini

If you found this project useful, feel free to ⭐ the repository.

