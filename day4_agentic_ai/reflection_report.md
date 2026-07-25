# Day 4 Reflection Report: Autonomous Agentic AI Architecture

## 🎯 Executive Summary
Day 4 focused on implementing an autonomous AI Agent using the **ReAct (Reasoning + Acting)** framework. The agent autonomously breaks complex goals into sequential sub-tasks, selects appropriate tools (calculator, text statistics, currency conversion), observes intermediate tool outputs, and maintains conversation memory across turns.

---

## 🛠️ ReAct Loop Mechanics & Findings

1. **Thought-Action-Observation Loop**:
   - Forcing the model to explicitly write out `Thought:`, `Action:`, and `Action Input:` before emitting a final answer prevents premature assumptions and guarantees tool parameters are well-formed.
2. **Handling Multi-Tool Chaining**:
   - In compound queries (e.g. math calculation followed by currency conversion), the agent successfully feeds step 1 observations into step 2 tool inputs without user re-prompting.
3. **Loop Safeguards**:
   - Enforced a hard `max_steps` threshold (default 5) to prevent infinite looping when tools return unexpected error strings.
