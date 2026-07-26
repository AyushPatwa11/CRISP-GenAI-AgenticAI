import sys
import os
import json
import streamlit as st
from dotenv import load_dotenv

# Ensure local script directory is first in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_bridge import MCPToolRegistry
from external_tools import get_live_weather, search_web_duckduckgo, create_calendar_invite_mock

load_dotenv()

st.set_page_config(
    page_title="OmniTool MCP - Tool & Protocol Bridge",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 OmniTool MCP — Real-Time API & Protocol Bridge")
st.caption("Connect LLMs to Real-Time Web APIs, Live Weather Services, and Standardized MCP Tool Servers")

# Initialize MCP Registry
registry = MCPToolRegistry()

# Register Tools
registry.register_tool(
    name="get_live_weather",
    description="Fetches real-time temperature and wind speed for any city using Open-Meteo REST API.",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. 'Bhilai', 'London', 'Tokyo'"}
        },
        "required": ["city"]
    },
    func=lambda args: get_live_weather(args.get("city", "Bhilai"))
)

registry.register_tool(
    name="search_web_duckduckgo",
    description="Performs live web search for news, release dates, stocks, and general information.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Web search query string"}
        },
        "required": ["query"]
    },
    func=lambda args: search_web_duckduckgo(args.get("query", "Agentic AI"))
)

registry.register_tool(
    name="create_calendar_invite",
    description="Schedules a calendar meeting invite with title, date, and attendees.",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Meeting title"},
            "date_str": {"type": "string", "description": "Date & time string"},
            "attendees": {"type": "string", "description": "Comma-separated emails"}
        },
        "required": ["title", "date_str", "attendees"]
    },
    func=lambda args: create_calendar_invite_mock(args.get("title", "Sync"), args.get("date_str", "Tomorrow 3pm"), args.get("attendees", "user@example.com"))
)

# Sidebar
st.sidebar.header("⚙️ LLM & MCP Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password")

# Tabs
tab1, tab2, tab3 = st.tabs(["🧪 Direct Tool Testing", "📋 MCP Schema Inspector", "🤖 Agent Assistant Mode"])

with tab1:
    st.markdown("### 🛠️ Test External Real-World Tools Directly")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌦️ Real-Time Weather API (Open-Meteo)")
        city_input = st.text_input("City Name", value="Bhilai")
        if st.button("Fetch Live Weather"):
            with st.spinner("Calling Open-Meteo REST API..."):
                res = get_live_weather(city_input)
                st.info(res)
                
    with col2:
        st.markdown("#### 🔍 Live Web Search (DuckDuckGo)")
        search_query = st.text_input("Search Query", value="Latest breakthroughs in Agentic AI 2026")
        if st.button("Execute Web Search"):
            with st.spinner("Searching live web via DDGS..."):
                res = search_web_duckduckgo(search_query)
                st.markdown(res)

with tab2:
    st.markdown("### 📋 Model Context Protocol (MCP) JSON Schemas")
    st.caption("Standardized MCP tool definitions generated dynamically for AI model tool calling.")
    schemas = registry.get_all_schemas()
    st.json(schemas)

with tab3:
    st.markdown("### 🤖 MCP-Enabled AI Assistant")
    st.caption("Enter a query requiring real-time tool execution (e.g. Weather, Release dates, Web Search).")
    
    st.caption("💡 Quick Sample Presets (Click to auto-fill):")
    pcols = st.columns(3)
    preset_query = ""
    if pcols[0].button("🌦️ Live Bhilai Weather"):
        preset_query = "What is the current weather in Bhilai right now?"
    if pcols[1].button("🎬 Spider-Man Release Date"):
        preset_query = "When is Spider-Man: Brand New Day releasing?"
    if pcols[2].button("💻 Python 3.14 Features"):
        preset_query = "Search for Python 3.14 new features."

    user_prompt = st.text_area(
        "User Instruction",
        height=90,
        value=preset_query if preset_query else "What is the current weather in Bhilai and search for recent news about AI agents."
    )
    
    if st.button("🚀 Process Instruction via Tool Engine", type="primary"):
        if not api_key.strip():
            st.error("Please provide a valid API key in the sidebar.")
        elif not user_prompt.strip():
            st.error("Please enter a user instruction.")
        else:
            with st.status("⚡ Running Fast MCP Tool Engine...", expanded=True) as status_box:
                try:
                    status_box.update(label="🤖 Step 1: Connecting to LLM & evaluating tool schemas...")
                    if provider == "Groq":
                        from langchain_groq import ChatGroq
                        llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                    else:
                        from langchain_openai import ChatOpenAI
                        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                    mcp_schemas_text = json.dumps(schemas, indent=2)
                    system_instructions = f"""You are an MCP-Enabled AI Assistant.
Available MCP Tools JSON Schema:
{mcp_schemas_text}

Rules:
If the request requires external information or action, choose the tool and argument parameters from the schema.
Return JSON with format:
{{
  "tool_call": "tool_name",
  "arguments": {{ "arg1": "val1" }},
  "reasoning": "Why this tool is chosen"
}}
If no tool is needed, return:
{{
  "tool_call": null,
  "direct_answer": "your direct answer here"
}}
"""
                    response = llm.invoke(f"{system_instructions}\n\nUser Request: {user_prompt}")
                    content = response.content.strip()
                    
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                        
                    parsed = json.loads(content)
                    
                    if parsed.get("tool_call"):
                        tool_name = parsed["tool_call"]
                        args = parsed.get("arguments", {})
                        
                        status_box.update(label=f"🌐 Step 2: Executing tool `{tool_name}` with parameters...")
                        
                        st.markdown(f"**🔧 Tool Triggered:** `{tool_name}`")
                        st.markdown(f"**💭 Reasoning:** {parsed.get('reasoning', '')}")
                        st.json(args)
                        
                        tool_result = registry.execute_mcp_call(tool_name, args)
                        
                        st.markdown("### 📥 Tool Execution Output")
                        st.success(tool_result)
                        
                        status_box.update(label="✨ Step 3: Generating final answer...")
                        synth_prompt = f"Original Query: {user_prompt}\nTool Executed: {tool_name}\nTool Output: {tool_result}\nSynthesize a clear final user response:"
                        final_res = llm.invoke(synth_prompt)
                        
                        status_box.update(label="✅ Tool Engine Execution Complete!", state="complete")
                        
                        st.markdown("### 🌟 Final Synthesized Answer")
                        st.write(final_res.content)
                    else:
                        status_box.update(label="✅ Answer Generated!", state="complete")
                        st.markdown("### 🌟 Direct Answer")
                        st.write(parsed.get("direct_answer", content))
                        
                except Exception as e:
                    status_box.update(label="❌ Tool Execution Failed", state="error")
                    st.error(f"Execution Error: {str(e)}")
