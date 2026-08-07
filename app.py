from pathlib import Path
import streamlit as st
from backend import create_conversation_chain

files_folder = Path(__file__).parent / "files"
files_folder.mkdir(exist_ok=True)


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
    with st.sidebar:
        st.header("Upload PDFs")
        uploaded_pdfs = st.file_uploader(
            "Add PDF files",
            type="pdf",
            accept_multiple_files=True
        )
        if uploaded_pdfs:
            save_uploaded_files(uploaded_pdfs, files_folder)
            st.success(f"{len(uploaded_pdfs)} file(s) saved successfully!")

        button_label = "Initialize Chat"
        if "chain" in st.session_state:
            button_label = "Update Chat"
        if st.button(button_label, use_container_width=True):
            if len(list(files_folder.glob("*.pdf"))) == 0:
                st.error("Add PDF files to initialize chat")
            else:
                st.success("Initializing Chat...")
                create_conversation_chain()
                st.rerun()
    chat_app()


if __name__ == "__main__":
    main()