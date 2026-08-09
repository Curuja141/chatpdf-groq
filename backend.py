import io
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image

_ = load_dotenv(find_dotenv())

# Available Groq models (free tier, see console.groq.com for the up-to-date list)
model_name = "llama-3.3-70b-versatile"

# Below this many characters, we treat the page's embedded text layer as
# "effectively empty" (e.g. a stray header on an otherwise scanned page)
# and fall back to OCR instead of trusting it.
MIN_TEXT_LENGTH = 20

# Higher DPI = better OCR accuracy but slower rendering. 300 is the standard
# sweet spot for OCR engines like Tesseract.
OCR_DPI = 300

# Tesseract language packs to use. "por+eng" covers PT-BR and English source
# documents; extend this if you expect other languages.
OCR_LANGUAGES = "por+eng"


def extract_page_text(page: fitz.Page) -> tuple[str, bool]:
    """Returns (text, used_ocr) for a single PDF page.

    Tries the page's native text layer first (fast, free, no dependencies).
    Only falls back to OCR when that layer is missing or too short to be
    useful -- the signature of a scanned/image-only page.
    """
    text = page.get_text().strip()
    if len(text) >= MIN_TEXT_LENGTH:
        return text, False

    pixmap = page.get_pixmap(dpi=OCR_DPI)
    image = Image.open(io.BytesIO(pixmap.tobytes("png")))
    ocr_text = pytesseract.image_to_string(image, lang=OCR_LANGUAGES)
    return ocr_text.strip(), True


def load_documents(session_folder: Path) -> list[Document]:
    documents = []
    ocr_page_count = 0

    for file in session_folder.glob("*.pdf"):
        pdf = fitz.open(file)
        for page_number, page in enumerate(pdf, start=1):
            text, used_ocr = extract_page_text(page)
            if used_ocr:
                ocr_page_count += 1
            if not text:
                continue
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file.name,
                        "page": page_number,
                        "ocr": used_ocr,
                    },
                )
            )
        pdf.close()

    if ocr_page_count:
        st.info(f"{ocr_page_count} page(s) required OCR (scanned/image content detected).")

    return documents


def split_documents(documents):
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    documents = recursive_splitter.split_documents(documents)
    for i, doc in enumerate(documents):
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
    with st.spinner("Reading PDFs... scanned pages take longer (OCR)."):
        documents = load_documents(session_folder)
        documents = split_documents(documents)

    if not documents:
        st.error(
            "Couldn't extract any text from the uploaded PDF(s), even with OCR. "
            "This can happen with very low-resolution scans, handwritten pages, "
            "or corrupted files. Please try a clearer PDF."
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