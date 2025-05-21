<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>YouTube Chatbot</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 40px;
      background-color: #f9f9f9;
      color: #333;
      line-height: 1.6;
    }
    h1, h2 {
      color: #1a73e8;
    }
    code {
      background-color: #eee;
      padding: 2px 5px;
      border-radius: 4px;
    }
    pre {
      background-color: #272822;
      color: #f8f8f2;
      padding: 10px;
      border-radius: 5px;
      overflow-x: auto;
    }
    ul {
      list-style: square;
      padding-left: 20px;
    }
    .folder-structure {
      font-family: monospace;
      background-color: #f0f0f0;
      padding: 10px;
      border-left: 3px solid #1a73e8;
    }
    a {
      color: #1a73e8;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <h1>📺 YouTube Video Chatbot</h1>
  <p>An intelligent chatbot that allows users to ask questions about any YouTube video and get meaningful answers using <strong>LangChain</strong>, <strong>FAISS</strong>, <strong>HuggingFace</strong>, and <strong>OpenAI GPT</strong>.</p>

  <h2>🚀 Features</h2>
  <ul>
    <li>🔍 Extracts transcript from YouTube videos</li>
    <li>🧠 Converts transcripts into vector embeddings using HuggingFace</li>
    <li>📚 Stores and queries transcript chunks via FAISS vector store</li>
    <li>💬 Answers user questions using OpenAI's GPT model</li>
    <li>🖥️ Built using <strong>LangChain</strong>, <strong>Streamlit</strong>, and <strong>HuggingFace</strong></li>
  </ul>

  <h2>🧰 Tech Stack</h2>
  <ul>
    <li>Python 3.10+</li>
    <li>LangChain</li>
    <li>langchain-community</li>
    <li>HuggingFace Transformers & Embeddings</li>
    <li>FAISS</li>
    <li>OpenAI</li>
    <li>Streamlit</li>
  </ul>

  <h2>📦 Installation</h2>
  <pre><code>git clone https://github.com/yourusername/youtube-chatbot.git
cd youtube-chatbot

# Create virtual environment

python -m venv venv
venv\Scripts\activate # Windows

# OR

source venv/bin/activate # macOS/Linux

# Install dependencies

pip install -r requirements.txt

# Set API Key

# Create a .env file and add:

OPENAI_API_KEY=your_openai_key</code></pre>

  <h2>▶️ Usage</h2>
  <pre><code>streamlit run chatbot.py</code></pre>
  <p>Then open the link provided in your browser.</p>

  <h2>📁 Project Structure</h2>
  <div class="folder-structure">
    .
    ├── chatbot.py            # Main Streamlit app<br>
    ├── requirements.txt      # Python dependencies<br>
    ├── .env                  # OpenAI API key<br>
    └── README.html           # Documentation
  </div>

  <h2>🧪 Sample YouTube Links</h2>
  <ul>
    <li><a href="https://www.youtube.com/watch?v=8mAITcNt710" target="_blank">CS50 Lecture</a></li>
    <li><a href="https://www.youtube.com/watch?v=GM4Ye0ZdgD4" target="_blank">LLM Tutorial</a></li>
  </ul>

  <h2>✅ To-Do / Improvements</h2>
  <ul>
    <li>Add support for non-English transcripts</li>
    <li>Enable chat history</li>
    <li>Multi-video support</li>
    <li>Offline transcript support</li>
  </ul>

  <h2>🙌 Acknowledgments</h2>
  <ul>
    <li><a href="https://www.langchain.com/" target="_blank">LangChain</a></li>
    <li><a href="https://openai.com/" target="_blank">OpenAI</a></li>
    <li><a href="https://github.com/facebookresearch/faiss" target="_blank">FAISS</a></li>
    <li><a href="https://huggingface.co/" target="_blank">HuggingFace</a></li>
    <li><a href="https://github.com/jdepoix/youtube-transcript-api" target="_blank">YouTubeTranscriptAPI</a></li>
  </ul>

  <h2>📜 License</h2>
  <p>MIT License</p>

</body>
</html>
