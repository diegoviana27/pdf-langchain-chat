"""
search.py – Módulo de busca semântica no pgVector.

Pode ser usado como módulo (importado por chat.py) ou executado
diretamente para testes rápidos:

    python src/search.py "Qual o faturamento da empresa?"
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from langchain_postgres import PGVector
import config

# ── Prompt template ──────────────────────────────────────────────────────────

PROMPT_TEMPLATE = """CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def get_vector_store() -> PGVector:
    """Retorna uma instância conectada ao PGVector."""
    embeddings = config.get_embeddings()
    return PGVector(
        embeddings=embeddings,
        collection_name=config.COLLECTION_NAME,
        connection=config.CONNECTION_STRING,
        use_jsonb=True,
    )


def search_documents(query: str, k: int = config.SEARCH_K) -> list:
    """
    Busca os k chunks mais relevantes para a query.
    Retorna lista de tuplas (Document, score).
    """
    store = get_vector_store()
    results = store.similarity_search_with_score(query, k=k)
    return results


def build_context(results: list) -> str:
    """Concatena o conteúdo dos documentos retornados numa string de contexto."""
    parts = []
    for i, (doc, score) in enumerate(results, start=1):
        parts.append(f"[Trecho {i} | score={score:.4f}]\n{doc.page_content}")
    return "\n\n".join(parts)


def answer_question(question: str) -> str:
    """
    Pipeline completo:
      1. Vetoriza a pergunta
      2. Busca os k chunks mais relevantes
      3. Monta o prompt
      4. Chama a LLM
      5. Retorna a resposta
    """
    results = search_documents(question)

    if not results:
        return "Não tenho informações necessárias para responder sua pergunta."

    context = build_context(results)
    prompt  = PROMPT_TEMPLATE.format(context=context, question=question)

    llm      = config.get_llm()
    response = llm.invoke(prompt)

    # ChatOpenAI / ChatGoogleGenerativeAI retornam um AIMessage
    if hasattr(response, "content"):
        return response.content.strip()
    return str(response).strip()


# ── Execução direta (teste) ──────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/search.py \"Sua pergunta aqui\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    print(f"\nPERGUNTA: {question}")
    print(f"RESPOSTA: {answer_question(question)}\n")
