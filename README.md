# 📄 Ingestão e Busca Semântica com LangChain + pgVector

Pipeline completo para ingestão de PDFs e busca semântica via CLI, utilizando **LangChain**, **PostgreSQL + pgVector** e modelos da **OpenAI** ou **Google Gemini**.

---

## 🗂️ Estrutura do projeto

```
├── docker-compose.yml     # Sobe o PostgreSQL com pgVector
├── requirements.txt       # Dependências Python
├── .env.example           # Template de variáveis de ambiente
├── src/
│   ├── config.py          # Configurações centralizadas (lida pelo .env)
│   ├── ingest.py          # Ingestão do PDF → chunks → embeddings → pgVector
│   ├── search.py          # Busca semântica + chamada à LLM
│   └── chat.py            # Interface CLI interativa
├── document.pdf           # PDF a ser ingerido
└── README.md
```

---

## ⚙️ Pré-requisitos

| Ferramenta | Versão mínima |
|------------|---------------|
| Python     | 3.10+         |
| Docker     | 24+           |
| Docker Compose | v2+      |

---

## 🚀 Instalação e configuração

### 1. Clone o repositório

```bash
git clone https://github.com/diegoviana27/pdf-langchain-chat.git
cd pdf-langchain-chat
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate          # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas chaves:

```env
# Provedor: "openai" ou "gemini"
AI_PROVIDER=openai

# Chave OpenAI (se AI_PROVIDER=openai)
OPENAI_API_KEY=sk-...

# Chave Google (se AI_PROVIDER=gemini)
GEMINI_API_KEY=...

# Banco de dados (padrão compatível com o docker-compose)
POSTGRES_USER=langchain
POSTGRES_PASSWORD=langchain
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=langchain_db

# PDF a ser ingerido
PDF_PATH=document.pdf
```

### 5. Coloque o PDF na raiz do projeto

Renomeie ou aponte seu PDF como `document.pdf` (ou ajuste `PDF_PATH` no `.env`).

---

## ▶️ Ordem de execução

### 1. Suba o banco de dados

```bash
docker compose up -d
```

Aguarde alguns segundos até o container ficar saudável:

```bash
docker compose ps   # Status deve ser "healthy"
```

### 2. Ingira o PDF

```bash
python src/ingest.py
```

Opções disponíveis:

```bash
python src/ingest.py --pdf outro_arquivo.pdf   # PDF alternativo
python src/ingest.py --reset                   # Apaga a coleção antes de ingerir
```

Saída esperada:

```
[INFO] Carregando PDF: document.pdf
[INFO] Páginas carregadas: 12
[INFO] Total de chunks gerados: 47
[INFO] Provedor de IA: OPENAI
[INFO] Conectando ao banco de dados...
[INFO] Gerando embeddings e salvando no banco... (pode demorar)
[OK] Ingestão concluída! 47 chunks armazenados na coleção 'pdf_documents'.
```

### 3. Inicie o chat

```bash
python src/chat.py
```

---

## 💬 Exemplo de uso do chat

```
╔══════════════════════════════════════════════════════════════╗
║        Chat com PDF  •  LangChain + pgVector                 ║
║  Provedor: OPENAI                                            ║
║  Coleção : pdf_documents                                     ║
╚══════════════════════════════════════════════════════════════╝
  Digite sua pergunta e pressione Enter.
  Para sair: 'sair', 'exit' ou Ctrl+C.

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

────────────────────────────────────────────────────────────────

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

────────────────────────────────────────────────────────────────

PERGUNTA: sair
[INFO] Encerrando. Até logo!
```

---

## 🔍 Teste de busca sem chat

Você pode testar uma pergunta avulsa diretamente:

```bash
python src/search.py "Qual é a receita bruta anual?"
```

---

## 🛠️ Detalhes técnicos

| Parâmetro | Valor |
|-----------|-------|
| Chunk size | 1 000 caracteres |
| Chunk overlap | 150 caracteres |
| k (resultados) | 10 |
| Embedding OpenAI | `text-embedding-3-small` |
| Embedding Gemini | `models/gemini-embedding-001` |
| LLM OpenAI | `gpt-4o-mini` |
| LLM Gemini | `gemini-2.5-flash-lite` |
| Banco | PostgreSQL 16 + pgVector |

> **Nota:** O modelo `gpt-5-nano` não está disponível publicamente no momento da criação deste projeto. O `gpt-4o-mini` oferece custo-benefício equivalente. Substitua em `src/config.py` quando o modelo for lançado.

---

## 🐳 Comandos Docker úteis

```bash
docker compose up -d        # Sobe o banco em background
docker compose down         # Para e remove os containers
docker compose down -v      # Remove também o volume (apaga dados)
docker compose logs -f      # Acompanha os logs
```

---

## 📝 Licença

MIT
