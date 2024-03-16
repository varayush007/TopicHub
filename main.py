# import streamlit as st
# from articles import articles
# from youtube import youtube_summary
#
# st.title("TopicHub 🎥")
# with st.expander("Click to view rules"):
#     st.markdown("This is an End to End LLM Project Made using Langchain. User initially have 2 choices either they can "
#                 "directly talk with the new articles whether it is summarization or QnA related to  it, up to 3 URLs "
#                 "are"
#                 "supported and another one is User can input the Youtube Video Link and the summary for the video ill "
#                 "be"
#                 "provided. LLM Model used - Open AI")
#
# st.sidebar.title("Functionalities")
# if st.sidebar.button("News Articles"):
#     main_placeholder = st.empty()
#     articles()
#
# if st.sidebar.button("Youtube Video Summarization"):
#     main_placeholder = st.empty()
#     youtube_summary()


import streamlit as st
from articles import articles
from youtube import youtube_summary

# --- State Management ---
if "show_homepage_content" not in st.session_state:
    st.session_state.show_homepage_content = True  # Initial state


# --- Main Page Content ---
def display_homepage_content():
    st.title("TopicHub 🎥")
    with st.expander("Click to view rules"):
        st.markdown(
            "This is an End to End LLM Project Made using Langchain. User initially have 2 choices either they can "
            "directly talk with the new articles whether it is summarization or QnA related to  it, "
            "up to 3 URLs"
            "are"
            "supported and another one is User can input the Youtube Video Link and the summary for the "
            "video ill"
            "be"
            "provided. LLM Model used - Open AI")


# --- Sidebar ---
st.sidebar.title("Functionalities")

if st.sidebar.button("Homepage"):
    st.session_state.show_homepage_content = True
if st.sidebar.button("News Articles"):
    st.session_state.show_homepage_content = False
    main_placeholder = st.empty()
    articles()
if st.sidebar.button("Youtube Video Summarization"):
    st.session_state.show_homepage_content = False
    main_placeholder = st.empty()
    youtube_summary()

# --- Display Content based on State---
if st.session_state.show_homepage_content:
    display_homepage_content()
