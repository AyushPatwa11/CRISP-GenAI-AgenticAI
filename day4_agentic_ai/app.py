import streamlit as st
import os
from dotenv import load_dotenv
from agent import ReActAgent

load_dotenv()

st.set_page_config(
    page_title="AgentFlow AI - Autonomous ReAct Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AgentFlow AI — Autonomous ReAct Agent & Visual Trace")
st.caption("ReAct (Reasoning + Acting) Agent featuring Tool Invocation, Working Memory, and Step-by-Step Execution Traces")

# Sidebar Configuration
st.sidebar.header("⚙️ Agent & Provider Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password")
max_steps = st.sidebar.slider("Max Reasoning Steps", 1, 10, 5)

st.sidebar.divider()
st.sidebar.markdown("### 🧰 Agent Tool Registry")
st.sidebar.info("1. 🧮 **Calculator**: Evaluates math expressions\n2. 📊 **Text Analyzer**: Word & sentence stats\n3. 💱 **Currency Converter**: USD to INR/EUR/GBP")

# Tool Cards Showcase
st.markdown("### 🧰 Available Agent Tools")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**🧮 Calculator**\n\nEvaluates math expressions safely (`1500 * 0.82 + 450`).")
with col2:
    st.info("**📊 Text Analyzer**\n\nComputes word count, character count & stats.")
with col3:
    st.info("**💱 Currency Converter**\n\nConverts USD to INR, EUR, GBP (`250 USD to INR`).")

st.divider()
st.markdown("### 🎯 User Goal & Task Execution")

# Sample Preset Goals
st.caption("💡 Quick Test Presets (Click any to auto-fill):")
preset_cols = st.columns(3)
selected_preset = ""

if preset_cols[0].button("💵 Currency + Tax Math"):
    selected_preset = "Convert $250 USD to INR, then add 18% GST tax on that converted amount."
if preset_cols[1].button("📊 Text Stats Analysis"):
    selected_preset = "Analyze text stats for: Artificial Intelligence is revolutionizing modern agentic workflows!"
if preset_cols[2].button("🧮 Multi-Step Calculation"):
    selected_preset = "Calculate 150 multiplied by 85, then add 450 to the result."

user_goal = st.text_area(
    "Enter a goal for the autonomous agent:",
    value=selected_preset if selected_preset else "Convert $250 USD to INR, then calculate a 18% tax on that total.",
    height=80,
    placeholder="e.g. Convert $100 USD to EUR and calculate 10% tip..."
)

if st.button("🚀 Execute Agent Goal", type="primary"):
    if not api_key.strip():
        st.error("Please enter your API Key in the sidebar.")
    elif not user_goal.strip():
        st.error("Please enter a valid goal for the agent.")
    else:
        with st.spinner("🤖 Autonomous Agent is reasoning, selecting tools, and solving goal..."):
            try:
                if provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                agent = ReActAgent(llm=llm)
                final_answer, traces = agent.run(user_goal, max_steps=max_steps)

                # 1. Prominent Final Answer Presentation (At the Top)
                st.success("✅ **Task Completed Successfully!**")
                
                st.markdown("## 🎯 Final Agent Answer")
                st.info(f"### {final_answer}")

                # 2. Executive Summary Metrics
                st.markdown("### 📊 Execution Summary")
                mcol1, mcol2, mcol3 = st.columns(3)
                tools_used = list(set([t['action'] for t in traces if t['action'] != "None (Finished)"]))
                mcol1.metric("⏱️ Steps Taken", f"{len(traces)} Steps")
                mcol2.metric("🛠️ Tools Called", len(tools_used))
                mcol3.metric("🏁 Agent Status", "Goal Achieved")

                st.divider()

                # 3. Clear Step-by-Step Visual Execution Flowchart
                st.markdown("### 🔍 Step-by-Step Execution Trace (Thought ➔ Action ➔ Observation)")
                st.caption("Here is how the AI agent planned and executed your task step by step:")

                for t in traces:
                    step_num = t['step']
                    action_name = t['action']
                    
                    if action_name == "None (Finished)" or "Direct" in action_name:
                        header_label = f"🏁 Step {step_num}: Goal Achieved & Final Response Generated"
                    else:
                        header_label = f"🛠️ Step {step_num}: Used Tool `{action_name}`"

                    with st.expander(header_label, expanded=True):
                        col_a, col_b = st.columns([1, 2])
                        with col_a:
                            st.markdown(f"**💭 Thinking Process:**")
                            st.caption(t['thought'])
                            if action_name != "None (Finished)":
                                st.markdown(f"**🔧 Tool Invoked:** `{action_name}`")
                                st.markdown(f"**📥 Input Sent:** `{t['action_input']}`")
                        with col_b:
                            st.markdown(f"**👁️ Tool Result / Observation:**")
                            st.code(t['observation'], language="text")

            except Exception as e:
                st.error(f"Agent execution failed: {str(e)}")
