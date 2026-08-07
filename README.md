# ChatPDF (Groq + LangChain + Streamlit)

A simple RAG (Retrieval-Augmented Generation) chat app that lets you upload PDF files and ask questions about their content, powered by **Groq** (free, fast LLM inference) instead of paid OpenAI APIs.

🇧🇷 [Versão em português abaixo](#chatpdf-groq--langchain--streamlit-1)

---

## Features

- Upload one or more PDF files
- Automatic text splitting and vector indexing (FAISS)
- Conversational memory (remembers previous questions in the session)
- Runs on **Groq's free LLM API** (Llama 3.3 70B)
- Uses a **local, free** HuggingFace embeddings model — no paid embeddings API needed

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [LangChain](https://www.langchain.com/) — RAG orchestration
- [Groq](https://groq.com/) — LLM inference (chat model)
- [HuggingFace Sentence Transformers](https://www.sbert.net/) — embeddings (runs locally)
- [FAISS](https://github.com/facebookresearch/faiss) — vector store

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your Groq API key

Get a free API key at [console.groq.com/keys](https://console.groq.com/keys), then create a `.env` file (you can copy `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your key:

```
GROQ_API_KEY=your_key_here
```

### 4. Run the app

```bash
streamlit run app.py
```

### 5. Use it

1. Upload one or more PDF files in the sidebar
2. Click **Initialize Chat**
3. Ask questions about your documents in the chat box

## Project Structure

```
.
├── app.py           # Streamlit UI
├── backend.py        # Document loading, embeddings, vector store, and chat chain
├── requirements.txt
├── .env.example
└── files/            # Uploaded PDFs are stored here (not tracked in git)
```

## Notes

- The first run will download the embeddings model (~90MB), which may take a moment.
- Groq does not offer an embeddings API, which is why this project uses a local HuggingFace model for that step — only the chat/LLM calls go through Groq.

## License

Feel free to use this project for learning or as a portfolio piece.

---

# ChatPDF (Groq + LangChain + Streamlit)

Um app de chat com RAG (Retrieval-Augmented Generation) simples que permite enviar arquivos PDF e fazer perguntas sobre o conteúdo, usando **Groq** (inferência de LLM gratuita e rápida) em vez de APIs pagas da OpenAI.

## Funcionalidades

- Upload de um ou mais arquivos PDF
- Divisão automática de texto e indexação vetorial (FAISS)
- Memória de conversa (lembra das perguntas anteriores na sessão)
- Roda na **API gratuita de LLM da Groq** (Llama 3.3 70B)
- Usa um modelo de embeddings **local e gratuito** do HuggingFace — sem necessidade de API paga

## Tecnologias

- [Streamlit](https://streamlit.io/) — interface
- [LangChain](https://www.langchain.com/) — orquestração do RAG
- [Groq](https://groq.com/) — inferência do LLM (modelo de chat)
- [HuggingFace Sentence Transformers](https://www.sbert.net/) — embeddings (roda localmente)
- [FAISS](https://github.com/facebookresearch/faiss) — banco de vetores

## Como Rodar

### 1. Clone o repositório

```bash
git clone <url-do-seu-repositorio>
cd <pasta-do-repositorio>
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure sua chave da API do Groq

Pegue uma chave gratuita em [console.groq.com/keys](https://console.groq.com/keys), depois crie um arquivo `.env` (você pode copiar o `.env.example`):

```bash
cp .env.example .env
```

Edite o `.env` e adicione sua chave:

```
GROQ_API_KEY=sua_chave_aqui
```

### 4. Rode a aplicação

```bash
streamlit run app.py
```

### 5. Como usar

1. Faça upload de um ou mais arquivos PDF na barra lateral
2. Clique em **Initialize Chat**
3. Faça perguntas sobre seus documentos na caixa de chat

## Estrutura do Projeto

```
.
├── app.py           # Interface Streamlit
├── backend.py        # Carregamento de documentos, embeddings, banco de vetores e chain de chat
├── requirements.txt
├── .env.example
└── files/            # PDFs enviados são armazenados aqui (não versionado no git)
```

## Observações

- A primeira execução vai baixar o modelo de embeddings (~90MB), o que pode demorar um pouco.
- O Groq não oferece API de embeddings, por isso este projeto usa um modelo local do HuggingFace para essa etapa — apenas as chamadas de chat/LLM passam pela Groq.

## Licença

Sinta-se à vontade para usar este projeto para aprendizado ou como peça de portfólio.
