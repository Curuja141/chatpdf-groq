# ChatPDF (Groq + LangChain + Streamlit)

A RAG-powered chat app to ask questions about your PDF documents — including scanned/image-only PDFs via OCR — using **Groq** (free, fast LLM inference) instead of paid OpenAI APIs.

🇧🇷 [Versão em português abaixo](#chatpdf-groq--langchain--streamlit-1)

---

## Features

- Upload one or more PDF files
- **OCR fallback for scanned PDFs** — pages with no text layer are automatically rendered and read via Tesseract OCR (PT-BR + English)
- Automatic text splitting and vector indexing (FAISS)
- Conversational memory (remembers previous questions in the session)
- **Per-session isolation** — each user gets their own private folder, so concurrent users never see or overwrite each other's uploaded PDFs
- Runs on **Groq's free LLM API** (Llama 3.3 70B)
- Uses a **local, free** HuggingFace embeddings model — no paid embeddings API needed, and cached in memory so it's only loaded once per app instance

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [LangChain](https://www.langchain.com/) — RAG orchestration
- [Groq](https://groq.com/) — LLM inference (chat model)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) — PDF parsing and page rendering
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via [pytesseract](https://github.com/madmaze/pytesseract) — text extraction for scanned pages
- [HuggingFace Sentence Transformers](https://www.sbert.net/) — embeddings (runs locally)
- [FAISS](https://github.com/facebookresearch/faiss) — vector store

## Getting Started

### 1. Clone the repository

```
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install Tesseract OCR (system dependency)

`pytesseract` is a wrapper around the Tesseract OCR engine — it needs to be installed separately from the Python packages below.

**Windows:**
Download and run the installer from [UB-Mannheim's Tesseract build](https://github.com/UB-Mannheim/tesseract/wiki), making sure to check the **Portuguese** language pack during setup. Then either add `C:\Program Files\Tesseract-OCR` to your system PATH, or point to it directly in `backend.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**macOS:**
```
brew install tesseract tesseract-lang
```

**Linux:**
```
sudo apt install tesseract-ocr tesseract-ocr-por
```

**Deploying to Streamlit Community Cloud:** the included `packages.txt` file installs Tesseract automatically — no extra setup needed there.

### 3. Install Python dependencies

```
pip install -r requirements.txt
```

### 4. Set up your Groq API key

Get a free API key at [console.groq.com/keys](https://console.groq.com/keys), then create a `.env` file (you can copy `.env.example`):

```
cp .env.example .env
```

Edit `.env` and add your key:

```
GROQ_API_KEY=your_key_here
```

### 5. Run the app

```
streamlit run app.py
```

### 6. Use it

1. Upload one or more PDF files in the sidebar (scanned PDFs work too — OCR kicks in automatically)
2. Click **Initialize Chat**
3. Ask questions about your documents in the chat box

## Project Structure

```
.
├── app.py             # Streamlit UI, per-session file handling
├── backend.py         # Document loading (with OCR fallback), embeddings, vector store, chat chain
├── requirements.txt
├── packages.txt        # System-level deps (Tesseract) for Streamlit Cloud deploy
├── .env.example
└── files/              # No longer used — replaced by per-session temp folders
```

## Notes

- The first run will download the embeddings model (~90MB), which may take a moment. It's cached afterward via `st.cache_resource`.
- Groq does not offer an embeddings API, which is why this project uses a local HuggingFace model for that step — only the chat/LLM calls go through Groq.
- OCR only runs on pages that lack a usable text layer, so regular text-based PDFs process just as fast as before. Scanned PDFs take longer per page since OCR is more computationally expensive than reading embedded text.
- Uploaded files are stored in a temporary folder unique to each browser session — not in a shared project folder — so concurrent users' documents never mix.

## License

Feel free to use this project for learning or as a portfolio piece.

---

# ChatPDF (Groq + LangChain + Streamlit)

Um app de chat com RAG (Retrieval-Augmented Generation) que permite enviar arquivos PDF — inclusive PDFs escaneados/imagem, via OCR — e fazer perguntas sobre o conteúdo, usando **Groq** (inferência de LLM gratuita e rápida) em vez de APIs pagas da OpenAI.

## Funcionalidades

- Upload de um ou mais arquivos PDF
- **OCR para PDFs escaneados** — páginas sem camada de texto são automaticamente renderizadas como imagem e lidas via Tesseract OCR (Português + Inglês)
- Divisão automática de texto e indexação vetorial (FAISS)
- Memória de conversa (lembra das perguntas anteriores na sessão)
- **Isolamento por sessão** — cada usuário tem sua própria pasta privada, então usuários simultâneos nunca veem ou sobrescrevem os PDFs uns dos outros
- Roda na **API gratuita de LLM da Groq** (Llama 3.3 70B)
- Usa um modelo de embeddings **local e gratuito** do HuggingFace — sem necessidade de API paga, e armazenado em cache para carregar apenas uma vez por instância do app

## Tecnologias

- [Streamlit](https://streamlit.io/) — interface
- [LangChain](https://www.langchain.com/) — orquestração do RAG
- [Groq](https://groq.com/) — inferência do LLM (modelo de chat)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) — leitura e renderização de páginas do PDF
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via [pytesseract](https://github.com/madmaze/pytesseract) — extração de texto de páginas escaneadas
- [HuggingFace Sentence Transformers](https://www.sbert.net/) — embeddings (roda localmente)
- [FAISS](https://github.com/facebookresearch/faiss) — banco de vetores

## Como Rodar

### 1. Clone o repositório

```
git clone <url-do-seu-repositorio>
cd <pasta-do-repositorio>
```

### 2. Instale o Tesseract OCR (dependência de sistema)

O `pytesseract` é apenas uma "ponte" em Python para o motor de OCR Tesseract — ele precisa ser instalado separadamente dos pacotes Python abaixo.

**Windows:**
Baixe e rode o instalador do [build da UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki), marcando o pacote de idioma **Portuguese** durante a instalação. Depois, adicione `C:\Program Files\Tesseract-OCR` ao PATH do sistema, ou aponte direto no `backend.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**macOS:**
```
brew install tesseract tesseract-lang
```

**Linux:**
```
sudo apt install tesseract-ocr tesseract-ocr-por
```

**Deploy no Streamlit Community Cloud:** o arquivo `packages.txt` incluído instala o Tesseract automaticamente — não precisa de configuração extra lá.

### 3. Instale as dependências Python

```
pip install -r requirements.txt
```

### 4. Configure sua chave da API do Groq

Pegue uma chave gratuita em [console.groq.com/keys](https://console.groq.com/keys), depois crie um arquivo `.env` (você pode copiar o `.env.example`):

```
cp .env.example .env
```

Edite o `.env` e adicione sua chave:

```
GROQ_API_KEY=sua_chave_aqui
```

### 5. Rode a aplicação

```
streamlit run app.py
```

### 6. Como usar

1. Faça upload de um ou mais arquivos PDF na barra lateral (PDFs escaneados também funcionam — o OCR entra em ação automaticamente)
2. Clique em **Initialize Chat**
3. Faça perguntas sobre seus documentos na caixa de chat

## Estrutura do Projeto

```
.
├── app.py              # Interface Streamlit, tratamento de arquivos por sessão
├── backend.py          # Carregamento de documentos (com fallback de OCR), embeddings, vector store, chain de chat
├── requirements.txt
├── packages.txt         # Dependências de sistema (Tesseract) para deploy no Streamlit Cloud
├── .env.example
└── files/               # Não é mais usado — substituído por pastas temporárias por sessão
```

## Observações

- A primeira execução vai baixar o modelo de embeddings (~90MB), o que pode demorar um pouco. Depois fica em cache via `st.cache_resource`.
- O Groq não oferece API de embeddings, por isso este projeto usa um modelo local do HuggingFace para essa etapa — apenas as chamadas de chat/LLM passam pela Groq.
- O OCR só roda em páginas sem camada de texto utilizável, então PDFs de texto normal continuam processando na mesma velocidade de antes. PDFs escaneados demoram mais por página, já que OCR é mais custoso computacionalmente do que ler texto já embutido.
- Os arquivos enviados ficam numa pasta temporária exclusiva de cada sessão do navegador — não numa pasta compartilhada do projeto — então documentos de usuários simultâneos nunca se misturam.

## Licença

Sinta-se à vontade para usar este projeto para aprendizado ou como peça de portfólio.