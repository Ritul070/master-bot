import streamlit as st
import google.generativeai as genai
import json
import sqlite3
from tavily import TavilyClient

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = st.secrets["API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

tavily = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# THE TOOLS
# ==========================================
def calculate_math(expression):
    try: return str(eval(expression))
    except Exception as e: return f"Math Error: {e}"

def count_words(text):
    return str(len(text.split()))

def query_database(sql_query):
    try:
        # Connect to local file, or create in-memory if on cloud
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        # CLOUD SAFETY NET: Create table and add data if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER)''')
        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO employees (id, name, department, salary) VALUES (?, ?, ?, ?)", [
                (25124, 'Ritul', 'AI', 50), (25125, 'Dhruvi', 'AI', 60), (25126, 'Roshni', 'CSE', 5)
            ])
            conn.commit()

        # Execute the actual query
        cursor.execute(sql_query + " COLLATE NOCASE")
        rows = cursor.fetchall()
        conn.close()
        return str(rows)
    except Exception as e: return f"Database Error: {e}"
    
def search_web(query):
    try:
        response = tavily.search(
            query=query,
            search_depth="basic",
            max_results=2
        )

        results = response.get("results", [])

        if not results:
            return "No results found."

        summary = ""

        for i, result in enumerate(results, start=1):
            summary += (
                f"Result {i}\n"
                f"Title: {result.get('title')}\n"
                f"Summary: {result.get('content')}\n"
                f"Source: {result.get('url')}\n\n"
            )

        return summary

    except Exception as e:
        return f"Search Error: {e}"

# ==========================================
# STREAMLIT UI & SESSION STATE
# ==========================================
st.title("🤖 My Custom AI Agent")
st.write("I can do math, count words, query the employee database, and search the live web.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# THE ROUTER LOGIC
# ==========================================
prompt = st.chat_input("Ask me anything...")

if prompt:
    # 1. Save User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. The System Prompt
    system_prompt = """
        You are an AI routing agent.

        Reply ONLY with a valid JSON object.

        Available tools:

        {"tool":"calculator","input":"45 * 32"}

        {"tool":"word_counter","input":"hello world"}

        {"tool":"database","input":"SELECT * FROM employees WHERE department='AI'"}

        {"tool":"web_search","input":"Latest AI news"}

        {"tool":"none","input":"Hello! How can I help?"}

        Never reply with explanations.
        Never use markdown.
        Return JSON only.
        """

    # 3. Ask Gemini
    full_prompt = system_prompt + "\nUser Input: " + prompt
    response = model.generate_content(full_prompt)
    ai_thought = response.text.strip()

    # THE SANITIZER: Strip LLM Markdown backticks if they exist
    if ai_thought.startswith("```"):
        lines = ai_thought.split('\n')
        ai_thought = '\n'.join(lines[1:-1]).strip()

    # 4. Parse and Execute
    try:
        command = json.loads(ai_thought)
        tool_name = command.get("tool")
        tool_input = command.get("input")

        if tool_name == "calculator":
            final_answer = calculate_math(tool_input)

        elif tool_name == "word_counter":
            final_answer = count_words(tool_input)

        elif tool_name == "database":
            final_answer = query_database(tool_input)

        elif tool_name == "web_search":
            final_answer = search_web(tool_input)

        else:
            final_answer = tool_input

    except Exception as e:
        final_answer = f"Agent failed. AI raw output was: {ai_thought}"

    # 5. Display & Save Assistant Message
    with st.chat_message("assistant"):
        st.markdown(final_answer)
        
    st.session_state.messages.append({"role": "assistant", "content": final_answer})