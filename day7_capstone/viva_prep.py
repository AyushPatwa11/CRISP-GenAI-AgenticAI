VIVA_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the difference between Generative AI and Agentic AI?",
        "options": [
            "Generative AI creates content based on prompts, while Agentic AI autonomous plans, uses tools, and executes multi-step goals with memory.",
            "Generative AI only works on images, while Agentic AI works on code.",
            "Agentic AI is slower and does not use Neural Networks.",
            "There is no difference between Generative AI and Agentic AI."
        ],
        "correct_index": 0,
        "explanation": "Generative AI focuses on single-turn content synthesis (text/images/audio). Agentic AI builds upon GenAI by giving models autonomy, tools, memory, and a reasoning loop (e.g. ReAct) to execute multi-step objectives independently."
    },
    {
        "id": 2,
        "question": "Explain RAG (Retrieval-Augmented Generation) architecture.",
        "options": [
            "A fine-tuning method to update model weights directly.",
            "A system that retrieves external document chunks matching a user query from a vector database and feeds them into the LLM context for grounded answers.",
            "An agent that runs web searches on Google continuously.",
            "A image generation pipeline."
        ],
        "correct_index": 1,
        "explanation": "RAG enhances LLM outputs by converting documents into vector embeddings stored in a vector database (e.g. ChromaDB). Relevant chunks are retrieved at query time and provided as context to eliminate hallucinations."
    },
    {
        "id": 3,
        "question": "What are embeddings in vector databases?",
        "options": [
            "Compression algorithms that zip text files.",
            "Numerical high-dimensional vector representations of text/data that capture semantic meaning and relationships.",
            "Database table primary keys.",
            "Raw HTML strings."
        ],
        "correct_index": 1,
        "explanation": "Embeddings translate raw text into high-dimensional numerical vectors (e.g., 384 or 1536 dimensions) where semantically similar concepts sit close to each other in vector space."
    },
    {
        "id": 4,
        "question": "Why use vector databases instead of traditional relational SQL databases for RAG?",
        "options": [
            "SQL databases cannot store text strings.",
            "Vector databases perform fast high-dimensional nearest-neighbor similarity searches (like Cosine or HNSW) impossible with keyword-matching SQL queries.",
            "Vector databases are free while SQL is paid.",
            "Vector databases do not require memory."
        ],
        "correct_index": 1,
        "explanation": "Traditional SQL databases rely on exact keyword matches. Vector databases allow semantic similarity search, finding relevant content even when user queries use different synonyms or vocabulary."
    },
    {
        "id": 5,
        "question": "What is hallucination in LLMs and how do we mitigate it?",
        "options": [
            "When the model runs out of GPU RAM.",
            "When the model generates plausible-sounding but factually incorrect information; mitigated by RAG, grounded system prompts, and low temperature.",
            "When the model refuses to answer a question.",
            "When the API connection times out."
        ],
        "correct_index": 1,
        "explanation": "Hallucination happens when an LLM fabricates facts. It is mitigated by providing strict context via RAG, setting low temperature parameters (0.0-0.2), and requiring source citations."
    },
    {
        "id": 6,
        "question": "Explain Prompt Templates.",
        "options": [
            "Pre-defined parameterized string wrappers that format user inputs into structured, predictable prompts for LLMs.",
            "HTML layout templates for website design.",
            "Python functions that compile C++ code.",
            "Database table schemas."
        ],
        "correct_index": 0,
        "explanation": "Prompt templates (e.g. in LangChain) provide consistent structure, system guidelines, and output schemas while inserting variable inputs at runtime."
    },
    {
        "id": 7,
        "question": "What is the difference between Tools and Agents?",
        "options": [
            "Tools are deterministic functions (e.g. calculator, weather API), while Agents are LLM decision-makers that choose which tools to execute to accomplish a goal.",
            "Tools are written in Python, while Agents are written in C++.",
            "Agents are hardware servers, while Tools are software apps.",
            "There is no difference."
        ],
        "correct_index": 0,
        "explanation": "A tool is an executable function (e.g. calculate sum, search web). An agent is the reasoning entity that inspects user goals, plans execution steps, and calls tools when necessary."
    },
    {
        "id": 8,
        "question": "Explain memory in AI agents.",
        "options": [
            "System RAM inside the server.",
            "Mechanisms (e.g. ConversationBufferMemory, SQLite) that maintain past interaction history and observations across multiple agent execution steps.",
            "Hardware caches on GPUs.",
            "Static text files that cannot be edited."
        ],
        "correct_index": 1,
        "explanation": "Agent memory allows the system to retain conversational context, remember past tool observations, and make informed decisions over multi-turn interactions."
    },
    {
        "id": 9,
        "question": "Why use LangChain?",
        "options": [
            "It is a database for storing images.",
            "It provides a standardized framework, chains, document loaders, and vector store integrations to build LLM and RAG applications efficiently.",
            "It replaces Python as a programming language.",
            "It is a cloud server hosting platform."
        ],
        "correct_index": 1,
        "explanation": "LangChain offers modular abstractions for prompts, models, vector stores, output parsers, and agent tool execution, reducing boilerplate code in AI application development."
    },
    {
        "id": 10,
        "question": "What is Model Context Protocol (MCP)?",
        "options": [
            "A hardware protocol for GPU cables.",
            "An open standard protocol that standardizes how AI applications declare tool capabilities and connect securely to external data sources and API servers.",
            "A network firewall rule.",
            "A database indexing algorithm."
        ],
        "correct_index": 1,
        "explanation": "MCP standardizes the JSON schema interface for tool definitions, resources, and prompts, enabling AI agents to discover and invoke tools across diverse client and server platforms seamlessly."
    }
]
