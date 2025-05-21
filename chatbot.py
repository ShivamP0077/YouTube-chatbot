import streamlit as st
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
import google.generativeai as genai
import os
import time

# Configure environment for file watching (for streamlit auto-reload)
os.environ["WATCHFILES_FORCE_POLLING"] = "true"

# Initialize session states
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(page_title="YouTube Video Chatbot", layout="wide")
st.title("🎬 Chat with a YouTube Video")

# API Key management
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key and st.button("Set API Key"):
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-pro")
            st.session_state.model = model
            st.session_state.api_key_set = True
            st.success("API Key set successfully!")
        except Exception as e:
            st.error(f"Error setting API key: {e}")
    
    if st.session_state.transcript:
        st.download_button(
            label="Download Transcript",
            data=st.session_state.transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

# Helper function to get transcript
def get_transcript(video_url):
    parsed_url = urlparse(video_url)
    video_id = None

    if 'youtube.com' in parsed_url.netloc:
        video_id = parse_qs(parsed_url.query).get("v", [None])[0]
    elif 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path.lstrip("/")

    if not video_id:
        st.error("Invalid YouTube URL.")
        return None

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([i["text"] for i in transcript])
        return full_text
    except NoTranscriptFound:
        st.error("No transcript found for this video.")
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
    except VideoUnavailable:
        st.error("This video is unavailable.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None

# Process transcript and create vector store
def process_transcript(transcript_text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_text(transcript_text)
    documents = [Document(page_content=doc) for doc in docs]

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

# Format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Prompt template
prompt = PromptTemplate(
    template="""
You are a helpful assistant for a YouTube video chatbot.
Answer ONLY from the provided transcript context.
If the context is insufficient, just say you don't know.

Context from video transcript:
{context}

Chat History:
{chat_history}

Question: {question}
""",
    input_variables=["context", "question", "chat_history"],
)

# Main app layout
if not st.session_state.api_key_set:
    st.warning("Please enter your Gemini API key in the sidebar to continue.")
else:
    # URL input section
    with st.container():
        st.subheader("Step 1: Enter a YouTube Video URL")
        video_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Load Video"):
                if video_url:
                    with st.spinner("Fetching transcript and building knowledge base..."):
                        transcript = get_transcript(video_url)
                        if transcript:
                            st.session_state.transcript = transcript
                            retriever = process_transcript(transcript)
                            st.session_state.retriever = retriever
                            st.success("Ready to chat with the video!")
        with col2:
            if st.button("Clear"):
                st.session_state.retriever = None
                st.session_state.transcript = None
                st.session_state.messages = []
                st.experimental_rerun()

    # Chat interface section
    if st.session_state.retriever:
        st.subheader("Step 2: Chat About the Video")
        
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Accept user input
        if prompt := st.chat_input("Ask a question about the video..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                try:
                    # Format chat history for context
                    chat_history = ""
                    for msg in st.session_state.messages[:-1]:  # Exclude the current question
                        if msg["role"] == "user":
                            chat_history += f"Human: {msg['content']}\n"
                        else:
                            chat_history += f"Assistant: {msg['content']}\n"
                    
                    # Create chain
                    chain = (
                        RunnableLambda(
                            lambda q: {
                                "context": format_docs(st.session_state.retriever.invoke(q)),
                                "question": q,
                                "chat_history": chat_history
                            }
                        )
                        | RunnableLambda(
                            lambda d: prompt.format(
                                context=d["context"],
                                question=d["question"],
                                chat_history=d["chat_history"]
                            )
                        )
                        | RunnableLambda(
                            lambda p: st.session_state.model.generate_content(p).text
                        )
                    )
                    
                    # Generate response with simulated typing effect
                    answer = chain.invoke(prompt)
                    
                    # Simulate typing with a stream
                    for chunk in answer.split():
                        full_response += chunk + " "
                        time.sleep(0.01)
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    error_msg = f"Error generating response: {e}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {error_msg}"})
    
    # Display additional information when no video is loaded
    elif video_url == "":
        st.info("Enter a YouTube URL above to get started.")