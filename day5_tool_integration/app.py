import streamlit as st
import os
import json
from dotenv import load_dotenv
from mcp_bridge import MCPToolRegistry

load_dotenv()

st.set_page_config(
    page_title="OmniTool MCP - Tool & Protocol Bridge",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 OmniTool MCP — Real-Time API & Protocol Bridge")
st.caption("Connect LLMs to Real-Time Web APIs, Live Weather Services, and Standardized MCP Tool Servers")

# Initialize MCP registry
registry = MCPToolRegistry()

# Sidebar Settings
st.sidebar.header("⚙️ LLM & MCP Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password")

st.divider()

# Tab Layout: 1. Individual Tool Testing, 2. MCP Schema Inspector, 3. Assistant Mode
tab1, tab2, tab3 = st.tabs(["🧪 Direct Tool Testing", "📋 MCP Schema Inspector", "🤖 Agent Assistant Mode"])

with tab1:
    st.markdown("### 🛠️ Test External Real-World Tools Directly")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌦️ Real-Time Weather API (Open-Meteo)")
        city_input = st.text_input("City Name", value="Bhilai")
        if st.button("Fetch Live Weather"):
            with st.spinner("Calling Open-Meteo REST API..."):
                res = registry.execute_mcp_call("get_live_weather", {"city": city_input})
                st.success(res)
                
    with col2:
        st.markdown("#### 🔍 Live Web Search (DuckDuckGo)")
        search_input = st.text_input("Search Query", value="Latest breakthroughs in Agentic AI 2026")
        if st.button("Execute Web Search"):
            with st.spinner("Searching web..."):
                res = registry.execute_mcp_call("search_web", {"query": search_input})
                st.info(res)

with tab2:
    st.markdown("### 📋 Model Context Protocol (MCP) Standardized Schemas")
    st.caption("Standardized JSON schemas exposed by this application server for client-side tool discovery.")
    
    schemas = registry.list_mcp_schemas()
    st.json(schemas)

with tab3:
    st.markdown("### 🤖 MCP-Enabled AI Assistant")
    st.caption("Enter a query requiring real-time tool execution (e.g., 'What is the current weather in Bhilai and schedule a meeting titled Project Sync tomorrow at 3pm with somil@example.com?').")
    
    user_prompt = st.text_area("User Instruction", height=100, value="Check current weather in Bhilai and search for recent news about AI agents.")
    
    if st.button("🚀 Process Instruction via Tool Engine", type="primary"):
        if not api_key:
            st.error("Please provide a valid API key in the sidebar.")
        elif not user_prompt.strip():
            st.error("Please enter a user instruction.")
        else:
            with st.spinner("Assistant evaluating tool invocations..."):
                try:
                    if provider == "Groq":
                        from langchain_groq import ChatGroq
                        llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                    else:
                        from langchain_openai import ChatOpenAI
                        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                    # Dynamic tool execution prompt
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
                        
                        st.markdown(f"**🔧 Tool Triggered:** `{tool_name}`")
                        st.markdown(f"**💭 Reasoning:** {parsed.get('reasoning', '')}")
                        st.json(args)
                        
                        # Execute Tool
                        tool_result = registry.execute_mcp_call(tool_name, args)
                        
                        st.markdown("### 📥 Tool Execution Output")
                        st.success(tool_result)
                        
                        # Synthesize Final Answer
                        synth_prompt = f"Original Query: {user_prompt}\nTool Executed: {tool_name}\nTool Output: {tool_result}\nSynthesize a helpful final user response:"
                        final_res = llm.invoke(synth_prompt)
                        
                        st.markdown("### 🌟 Final Synthesized Answer")
                        st.write(final_res.content)
                    else:
                        st.markdown("### 🌟 Direct Answer")
                        st.write(parsed.get("direct_answer", content))
                        
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")
