# 🤖 AI Agent

An intelligent AI Agent built with **Python**, **Streamlit**, and **Google Gemini** that can understand user requests, automatically choose the correct tool, execute it, and return a natural language response.

The agent combines the reasoning capabilities of a Large Language Model with multiple Python tools, making it capable of handling different tasks through a single chat interface.

---

# 📌 Overview

This project demonstrates how an AI Agent can use **tool calling** to solve user queries instead of relying only on text generation.

The agent analyzes each user prompt, determines which tool is required, executes that tool, and presents the result in a conversational format.

### Available Tools

- 🌐 **Web Search** – Searches the internet for up-to-date information.
- 🧮 **Calculator** – Solves mathematical expressions.
- 📝 **Word Counter** – Counts the number of words in a given text.
- 🗄️ **Database Query** – Retrieves employee information from a SQLite database.

---

# 🏗️ Architecture

```text
                User
                  │
                  ▼
        Streamlit Chat Interface
                  │
                  ▼
         Google Gemini AI Model
                  │
      Determines Required Tool
                  │
      ┌───────────┼────────────┐
      │           │            │
      ▼           ▼            ▼
 Web Search   Calculator   Word Counter
      │
      └──────────────┐
                     ▼
             Database Query
                     │
                     ▼
          Tool Execution Result
                     │
                     ▼
        Gemini Generates Response
                     │
                     ▼
                  User
```

### Workflow

1. User enters a prompt.
2. Gemini analyzes the request.
3. Gemini selects the appropriate tool.
4. The selected Python function executes.
5. The result is sent back to Gemini.
6. Gemini generates a natural language response.
7. Streamlit displays the final answer.

---

# 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Model
- Google Gemini 2.5 Flash

### Database
- SQLite

### Libraries
- google-generativeai
- streamlit
- sqlite3
- json

---

# ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-agent.git
cd ai-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key

Create a `.streamlit/secrets.toml` file.

```toml
API_KEY = "YOUR_GEMINI_API_KEY"
```

### 4. Create the Database

Run the database setup script.

```bash
python setup_db.py
```

### 5. Start the Application

```bash
streamlit run app.py
```

### 6. Open the Browser

```
http://localhost:8501
```

---

# 🚀 Features

- Multi-tool AI Agent
- Automatic tool selection using Gemini
- Real-time web search
- Mathematical calculations
- Word counting
- SQLite database querying
- Interactive Streamlit interface
- Natural language responses

---

# 📂 Project Structure

```text
AI-Agent/
│
├── app.py
├── setup_db.py
├── company.db
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```
