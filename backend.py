from pathlib import Path

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain_classic.memory import ConversationBufferMemory
import streamlit as st
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Available Groq models (free tier, see console.groq.com for the up-to-date list)
model_name = "llama-3.3-70b-versatile"


def load_documents(session_folder: Path):
    documents = []
    for file in session_folder.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        file_documents = loader.load()
        documents.extend(file_documents)
    return documents


def split_documents(documents):
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    documents = recursive_splitter.split_documents(documents)
    for i, doc in enumerate(documents):
        doc.metadata["source"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["doc_id"] = i
    return documents


@st.cache_resource(show_spinner=False)
def get_embedding_model():
    # Groq doesn't provide an embeddings API, so we use a free local HuggingFace model.
    # Cached with st.cache_resource so the ~90MB model loads once per app instance,
    # not once per "Initialize/Update Chat" click.
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vector_store(documents):
    embedding_model = get_embedding_model()
    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model
    )
    return vector_store


def create_conversation_chain(session_folder: Path):
    documents = load_documents(session_folder)
    documents = split_documents(documents)

    if not documents:
        st.error(
            "Couldn't extract any text from the uploaded PDF(s). "
            "This usually happens with scanned PDFs (image-only, no text layer). "
            "Please try a different PDF with selectable text."
        )
        st.stop()

    vector_store = create_vector_store(documents)
    chat = ChatGroq(model=model_name)

    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )

    retriever = vector_store.as_retriever()

    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        verbose=True
    )

    st.session_state["chain"] = chat_chain
    return chat_chain