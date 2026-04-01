"""
ingest.py – Lê um PDF, divide em chunks e armazena os vetores no pgVector.

Uso:
    python src/ingest.py
    python src/ingest.py --pdf outro_arquivo.pdf   # sobrescreve PDF_PATH do .env
"""

import sys
import argparse
import os

# Permite importar config.py mesmo rodando de qualquer diretório
sys.path.insert(0, os.path.dirname(__file__))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

import config


def parse_args():
    parser = argparse.ArgumentParser(description="Ingestão de PDF no pgVector")
    parser.add_argument(
        "--pdf",
        default=None,
        help="Caminho para o arquivo PDF (padrão: PDF_PATH do .env)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Apaga a coleção existente antes de ingerir",
    )
    return parser.parse_args()


def ingest(pdf_path: str, reset: bool = False) -> None:
    # ── 1. Validação ────────────────────────────────────────────────────────
    if not os.path.exists(pdf_path):
        print(f"[ERRO] Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    print(f"[INFO] Carregando PDF: {pdf_path}")

    # ── 2. Carregamento do PDF ───────────────────────────────────────────────
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"[INFO] Páginas carregadas: {len(documents)}")

    # ── 3. Split em chunks ──────────────────────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"[INFO] Total de chunks gerados: {len(chunks)}")

    # ── 4. Embeddings ────────────────────────────────────────────────────────
    print(f"[INFO] Provedor de IA: {config.AI_PROVIDER.upper()}")
    embeddings = config.get_embeddings()

    # ── 5. Armazenamento no pgVector ─────────────────────────────────────────
    print("[INFO] Conectando ao banco de dados...")

    store = PGVector(
        embeddings=embeddings,
        collection_name=config.COLLECTION_NAME,
        connection=config.CONNECTION_STRING,
        use_jsonb=True,
    )

    if reset:
        print("[INFO] Resetando coleção existente...")
        store.delete_collection()
        store = PGVector(
            embeddings=embeddings,
            collection_name=config.COLLECTION_NAME,
            connection=config.CONNECTION_STRING,
            use_jsonb=True,
        )

    print("[INFO] Gerando embeddings e salvando no banco... (pode demorar)")
    store.add_documents(chunks)

    print(f"[OK] Ingestão concluída! {len(chunks)} chunks armazenados na coleção '{config.COLLECTION_NAME}'.")


def main():
    args = parse_args()
    pdf_path = args.pdf or config.PDF_PATH
    ingest(pdf_path=pdf_path, reset=args.reset)


if __name__ == "__main__":
    main()
