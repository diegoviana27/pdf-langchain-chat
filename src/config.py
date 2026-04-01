"""
config.py – Configurações centralizadas do projeto.
Carrega variáveis de ambiente e instancia embeddings + LLM
de acordo com o provedor escolhido (openai | gemini).
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Banco de dados ──────────────────────────────────────────────────────────

POSTGRES_USER     = os.getenv("POSTGRES_USER", "langchain")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "langchain")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB       = os.getenv("POSTGRES_DB", "langchain_db")

CONNECTION_STRING = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

COLLECTION_NAME = "pdf_documents"

# ── PDF ─────────────────────────────────────────────────────────────────────

PDF_PATH        = os.getenv("PDF_PATH", "document.pdf")
CHUNK_SIZE      = 1000
CHUNK_OVERLAP   = 150
SEARCH_K        = 10

# ── Provedor de IA ──────────────────────────────────────────────────────────

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()


def get_embeddings():
    """Retorna o modelo de embeddings configurado."""
    if AI_PROVIDER == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            task_type="retrieval_document" 
        )
    # padrão: openai
    from langchain_openai import OpenAIEmbeddings
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )


def get_llm():
    """Retorna o modelo de linguagem configurado."""
    if AI_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0,
        )
    # padrão: openai
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
    )
