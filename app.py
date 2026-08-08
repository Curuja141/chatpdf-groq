import tempfile
import uuid
from pathlib import Path

import streamlit as st

from backend import create_conversation_chain


def get_session_folder() -> Path:
    """Returns a folder unique to this user's browser session, creating it on first use.

    Using a UUID per session (instead of the old shared 'files/' folder) means two
    users chatting with the app at the same time never see or overwrite each
    other's PDFs.
    """
    if "session_folder" not in st.session_state:
        session_id = str(uuid.uuid4())
        folder = Path(tempfile.gettempdir()) / "chatpdf_sessions" / session_id
        folder.mkdir(parents=True, exist_ok=True)
        st.session_state["session_folder"] = folder
    return st.session_state["session_folder"]


def chat_app():
    st.header("Welcome to ChatPDF", divider=True)

    if "chain" not in st.session_state:
        st.error("Upload PDFs to get started")
        st.stop()

    chain = st.session_state["chain"]
    memory = chain.memory
    messages = memory.load_memory_variables({})["chat_history"]

    container = st.container()
    for message in messages:
        chat = container.chat_message(message.type)
        chat.markdown(message.content)

    new_message = st.chat_input("Chat with your documents")
    if new_message:
        chat = container.chat_message("human")
        chat.markdown(new_message)

        chat = container.chat_message("ai")
        chat.markdown("Generating answer")
        chain.invoke({"question": new_message})
        st.rerun()


def save_uploaded_files(uploaded_files, folder):
    for file in folder.glob("*.pdf"):
        file.unlink()
    for file in uploaded_files:
        (folder / file.name).write_bytes(file.read())


def main():
    session_folder = get_session_folder()

    with st.sidebar:
        st.header("Upload PDFs")
        uploaded_pdfs = st.file_uploader(
            "Add PDF files",
            type="pdf",
            accept_multiple_files=True
        )

        if uploaded_pdfs:
            save_uploaded_files(uploaded_pdfs, session_folder)
            st.success(f"{len(uploaded_pdfs)} file(s) saved successfully!")

        button_label = "Initialize Chat"
        if "chain" in st.session_state:
            button_label = "Update Chat"

        if st.button(button_label, use_container_width=True):
            if len(list(session_folder.glob("*.pdf"))) == 0:
                st.error("Add PDF files to initialize chat")
            else:
                st.success("Initializing Chat...")
                create_conversation_chain(session_folder)
                st.rerun()

    chat_app()


if __name__ == "__main__":
    main()