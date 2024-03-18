import os
import streamlit as st
import pickle
import time
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()


def articles():
    global data
    st.title("New Articles")
    st.sidebar.title("News Article URLs")

    urls = []
    for i in range(3):
        url = st.sidebar.text_input(f"URL {i+1}")
        urls.append(url)

    process_url_clicked = st.sidebar.button("Process URLs")
    file_path = "faiss_index.pkl"

    main_placeholder = st.empty()
    llm = OpenAI(temperature=0.9, max_tokens=500)

    if process_url_clicked:
        try:
            # load the data
            loader = UnstructuredURLLoader(urls=urls)
            main_placeholder.text("Data Loading Started ⏳⏳")
            data = loader.load()
            print("Data loaded successfully!")
            print("Data:", data)
        except Exception as e:
            print("Error loading data:", e)

        # data splitting
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        main_placeholder.text("Text Splitting Started ⏳⏳")
        docs = text_splitter.split_documents(data)

        # DEBUG: Print docs to check its contents
        print("Length of docs:", len(docs))
        print("Docs:", docs)

        # create embeddings through OpenAI and save it to FAISS index

        embeddings = OpenAIEmbeddings()
        vectorstore_openai = FAISS.from_documents(docs, embeddings)
        main_placeholder.text("Embedding Vector Started Building ⏳⏳")
        time.sleep(5)

        # save the FAISS index to a pickle file
        with open(file_path, "wb") as f:
            pickle.dump(vectorstore_openai, f)

    query = main_placeholder.text_input("Question: ")
    if query:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                vectorstore = pickle.load(f)
                chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
                result = chain({"question": query}, return_only_outputs=True)
                # result will be a dictionary of this format --> {"answer": "", "sources": [] }
                st.header("Answer")
                st.write(result["answer"])

                # Display sources, if available
                sources = result.get("sources", "")
                if sources:
                    st.subheader("Sources:")
                    sources_list = sources.split("\n")  # Split the sources by newline
                    for source in sources_list:
                        st.write(source)




