import streamlit as st
import os
from dotenv import load_dotenv
from agent import ReActAgent

load_dotenv()

st.set_page_config(
    page_title="Day 4 - Autonomous Agentic AI Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Day 4: Autonomous Agentic AI Workflow & Visual Trace")
st.caption("ReAct (Reasoning + Acting) Agent featuring Tool Invocation, Working Memory, and Step-by-Step Execution Traces")

# Sidebar settings
st.sidebar.header("⚙️ Agent & Provider Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password")
max_steps = st.sidebar.slider("Max Reasoning Steps", 2, 8, 5)

# Session state initialization
if "agent_memory" not in st.session_state:
    st.session_state.agent_memory = []

st.markdown("### 🧰 Available Agent Tools")
tcol1, tcol2, tcol3 = st.columns(3)
with tcol1:
    st.info("🧮 **Calculator**: Evaluates math expressions (`1500 * 0.82 + 450`).")
with tcol2:
    st.info("📊 **Text Analyzer**: Computes word count, character count & readability.")
with tcol3:
    st.info("💱 **Currency Converter**: Converts USD amounts to INR/EUR (`250 USD to INR`).")

st.divider()

# Sample Presets
st.markdown("### 🎯 User Goal Input")

sample_preset = st.selectbox(
    "Choose a Sample Multi-Step Goal or Type Below:",
    [
        "Custom Goal",
        "Calculate total price for 12 items at $45 each with 15% discount, then convert total USD to INR.",
        "Analyze the stats of this text: 'Agentic AI workflows combine memory, tools, and multi-step reasoning to execute complex goals autonomously without constant human intervention.'",
        "Convert 500 USD to INR and add 2500 INR tax."
    ]
)

default_goal_text = "" if sample_preset == "Custom Goal" else sample_preset

user_goal = st.text_area("Enter Goal / Multi-step Instruction", value=default_goal_text, height=100)

if st.button("🚀 Execute Autonomous Agent", type="primary", use_container_width=True):
    if not user_goal.strip():
        st.error("Please enter a valid goal for the agent.")
    elif not api_key:
        st.error("Please enter a valid API key in the sidebar.")
    else:
        with st.spinner("Agent initializing planning loop..."):
            try:
                if provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                agent = ReActAgent(llm=llm)
                final_answer, traces = agent.run(user_goal, max_steps=max_steps)

                st.success("Agent Goal Execution Completed!")

                # Render Visual Traces
                st.markdown("### 🔍 Execution Trace Log (Thought ➔ Action ➔ Observation)")
                for t in traces:
                    with st.expander(f"Step {t['step']}: Action -> `{t['action']}`", expanded=True):
                        st.markdown(f"**💭 Thought:** {t['thought']}")
                        st.markdown(f"**🔧 Action:** `{t['action']}`")
                        st.markdown(f"**📥 Action Input:** `{t['action_input']}`")
                        st.markdown(f"**👁️ Observation:** `{t['observation']}`")

                st.divider()
                st.markdown("### 🎯 Final Agent Answer")
                st.success(final_answer)

            except Exception as e:
                st.error(f"Agent execution failed: {str(e)}")
