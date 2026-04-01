"""
chat.py – Interface CLI para conversa com o PDF via LangChain + pgVector.

Uso:
    python src/chat.py

Digite 'sair', 'exit' ou pressione Ctrl+C para encerrar.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import config as config  # noqa: F401  (valida .env antes de tudo)
from search import answer_question

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║        Chat com PDF  •  LangChain + pgVector                 ║
║  Provedor: {provider:<48}  ║
║  Coleção : {collection:<48}  ║
╚══════════════════════════════════════════════════════════════╝
  Digite sua pergunta e pressione Enter.
  Para sair: 'sair', 'exit' ou Ctrl+C.
""".format(
    provider=config.AI_PROVIDER.upper(),
    collection=config.COLLECTION_NAME,
)

SEPARATOR = "\n" + "─" * 64 + "\n"


def main() -> None:
    print(BANNER)

    while True:
        try:
            question = input("PERGUNTA: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n[INFO] Encerrando. Até logo!")
            break

        if not question:
            continue

        if question.lower() in {"sair", "exit", "quit", "q"}:
            print("[INFO] Encerrando. Até logo!")
            break

        try:
            answer = answer_question(question)
        except Exception as exc:  # noqa: BLE001
            answer = f"[ERRO ao consultar] {exc}"

        print(f"RESPOSTA: {answer}")
        print(SEPARATOR)


if __name__ == "__main__":
    main()
