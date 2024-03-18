import os
import streamlit as st
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.llms import GooglePalm
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv


def youtube_summary():

    def summarize_youtube_video(video_url):
        """Summarizes a YouTube video using LangChain and Google Palm"""
        load_dotenv()  # Load your environment variables

        try:
            loader = YoutubeLoader.from_youtube_url(video_url)
            transcript = loader.load()

            splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_documents(transcript)

            llm = GooglePalm(google_api_key=os.getenv('GOOGLE_API_KEY'), temperature=0.6)
            summarize_chain = load_summarize_chain(llm=llm, chain_type="refine")

            # Full summarization
            full_summary = summarize_chain.run(chunks)
            return full_summary

        except Exception as e:
            return f"An error occurred during summarization: {e}"

    st.title("Youtube Video Summarizer 🔉🔊")
    video_url = st.text_input("Enter YouTube Video URL:")

    if st.button("Summarize"):
        if video_url:
            full_summary = summarize_youtube_video(video_url)
            st.subheader("Full Summary")
            st.markdown(full_summary)
        else:
            st.warning("Please enter a YouTube video URL.")
