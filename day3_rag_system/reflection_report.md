# Day 3 Reflection Report: Retrieval-Augmented Generation (RAG) Architecture

## 🎯 Executive Summary
Day 3 focused on developing an end-to-end RAG system capable of ingesting PDF/TXT documents, partitioning them into semantic vector chunks, storing vector representations in **ChromaDB**, and executing grounded conversational QA with source metadata citations.

---

## 📐 Vector Indexing & Chunking Trade-offs

1. **Chunk Size Selection**:
   - Tested chunk sizes of 500, 1000, and 2000 characters with an overlap of 200 characters using `RecursiveCharacterTextSplitter`.
   - **Finding**: 1000 character chunks with 200 overlap yielded the optimal balance between maintaining full sentence context and minimizing irrelevant tokens retrieved per query.
2. **Embedding Model Efficiency**:
   - Utilized `sentence-transformers/all-MiniLM-L6-v2` locally on CPU.
   - Fast 384-dimensional vector embeddings without incurring third-party API costs or latency.
3. **Citation & Anti-Hallucination**:
   - Constrained LLM generation by passing strict system instructions requiring explicit document source attribution. If facts are absent in ChromaDB chunks, the system safely responds with a fallback indicating insufficient context.
