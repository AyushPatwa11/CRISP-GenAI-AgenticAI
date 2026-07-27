import streamlit as st
import os
import time
from dotenv import load_dotenv
from agent import ReActAgent

load_dotenv()

st.set_page_config(
    page_title="CogniTrace AI - Autonomous ReAct Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom High-Aesthetic Agent Command Center Styling
st.markdown("""
<style>
    .agent-header {
        background: linear-gradient(135deg, #121212 0%, #1E1E2C 50%, #00E5FF 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0, 229, 255, 0.2);
    }
    .agent-header h1 { color: white !important; font-weight: 800; font-size: 2.2rem; margin: 0; }
    .agent-header p { color: rgba(255,255,255,0.9) !important; font-size: 1.05rem; margin-top: 6px; margin-bottom: 0; }
    
    .final-box {
        background: rgba(0, 230, 118, 0.08);
        border: 2px solid #00E676;
        border-radius: 14px;
        padding: 24px;
        margin: 20px 0;
    }
    
    .trace-card-thought {
        background: rgba(101, 31, 255, 0.08);
        border-left: 4px solid #7C4DFF;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    
    .trace-card-action {
        background: rgba(0, 229, 255, 0.08);
        border-left: 4px solid #00E5FF;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="agent-header">
    <h1>🤖 CogniTrace AI Command Center</h1>
    <p>Autonomous ReAct Agent Engine — Multi-Step Reasoning, Short-Term Memory & Live Visual Execution Traces</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/bot.png", width=64)
    st.header("⚙️ Agent & Provider Settings")
    
    provider = st.radio("Select Provider", ["Groq", "OpenAI"])
    if provider == "Groq":
        model_name = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        default_key = os.getenv("GROQ_API_KEY", "")
    else:
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
        default_key = os.getenv("OPENAI_API_KEY", "")

    api_key = st.text_input("API Key", value=default_key, type="password")
    max_steps = st.slider("Max Reasoning Steps", 1, 10, 5)

    st.divider()
    st.markdown("### 🧰 Registered Agent Tools")
    st.info("1. 🧮 **Calculator**: Math expressions\n2. 📊 **Text Analyzer**: Word & char stats\n3. 💱 **Currency Converter**: USD to INR/EUR/GBP")

# Tool Cards Showcase
st.markdown("### 🧰 Available Autonomous Tools")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**🧮 Safe Math Calculator**\n\nEvaluates expressions (`1500 * 0.82 + 450`).")
with col2:
    st.info("**📊 Text Analytics Tool**\n\nComputes word count, character count & stats.")
with col3:
    st.info("**💱 Currency Conversion Engine**\n\nConverts USD to INR, EUR, GBP (`250 USD to INR`).")

st.divider()
st.markdown("### 🎯 Autonomous Goal Execution")

# Sample Preset Goals Dropdown
sample_goals_library = [
    "--- Select a Sample Goal to Auto-Fill ---",
    "💵 Currency + Tax Math: Convert $250 USD to INR, then add 18% GST tax on that converted amount.",
    "💶 Currency Conversion: Convert $1200 USD to EUR and subtract 5% service fee.",
    "💷 Currency Tip Calculation: What is $500 USD in GBP, and what is a 10% tip on that amount?",
    "🧮 Multi-Step Math: Calculate 150 multiplied by 85, then add 450 to the result.",
    "📐 Geometry Math: Calculate 3.14159 * (14 * 14) and divide by 2.",
    "🔢 Complex Expression: Evaluate (250 * 4) + (800 / 4) - 150.",
    "📊 Text Stats: Analyze text stats for: Artificial Intelligence is revolutionizing modern agentic workflows!",
    "📝 Word & Char Count: Analyze word count and character count for: Generative AI and Agentic Systems are transforming software.",
    "🔤 Sentence Analysis: Calculate character count for: Building intelligent multi-tool autonomous agents with LangChain.",
    "🌐 Chained Multi-Tool: Convert $300 USD to INR, add 18% tax, and analyze word count of 'Payment completed'."
]

selected_goal_option = st.selectbox("💡 Sample Goals Library (Choose from 10+ Test Scenarios):", sample_goals_library)

default_text = "Convert $250 USD to INR, then calculate a 18% tax on that total."
if selected_goal_option != "--- Select a Sample Goal to Auto-Fill ---":
    default_text = selected_goal_option.split(": ", 1)[-1]

user_goal = st.text_area(
    "Enter or edit a goal for the autonomous agent:",
    value=default_text,
    height=80,
    placeholder="e.g. Convert $100 USD to EUR and calculate 10% tip..."
)

if st.button("🚀 Execute Agent Goal", type="primary", use_container_width=True):
    if not api_key.strip():
        st.error("Please enter your API Key in the sidebar.")
    elif not user_goal.strip():
        st.error("Please enter a valid goal for the agent.")
    else:
        start_time = time.time()
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
                elapsed = time.time() - start_time

                # Prominent Final Answer Presentation
                st.markdown("<div class='final-box'>", unsafe_allow_html=True)
                st.markdown("## 🌟 Final Agent Solution")
                st.write(f"### {final_answer}")
                st.markdown("</div>", unsafe_allow_html=True)

                # Metrics
                mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                mcol1.metric("Reasoning Steps", f"{len(traces)} Steps")
                mcol2.metric("Execution Latency", f"{elapsed:.2f}s")
                mcol3.metric("Agent Status", "Goal Achieved")
                mcol4.metric("Engine Provider", provider)

                st.divider()

                # Visual Traces Flow
                st.markdown("### 🧩 Visual ReAct Execution Trace Flow")
                st.caption("Step-by-step breakdown of how CogniTrace AI reasoned and executed tools:")

                for step_idx, trace in enumerate(traces, 1):
                    with st.expander(f"Step {step_idx}: Thought ➔ Action ➔ Observation", expanded=(step_idx == 1)):
                        tcol1, tcol2 = st.columns(2)
                        with tcol1:
                            st.markdown(f"<div class='trace-card-thought'><b>💭 Agent Reasoning (Thought):</b><br>{trace.get('thought', 'Thinking...')}</div>", unsafe_allow_html=True)
                        with tcol2:
                            st.markdown(f"<div class='trace-card-action'><b>🔧 Tool Invoked (Action):</b><br>`{trace.get('action', 'None')}` with args `{trace.get('action_input', {})}`</div>", unsafe_allow_html=True)

                        st.markdown(f"**📥 Environment Observation:**")
                        st.info(trace.get("observation", "None"))

            except Exception as e:
                st.error(f"❌ Execution Error: {str(e)}")
