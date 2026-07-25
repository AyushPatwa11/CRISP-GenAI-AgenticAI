from typing import List, Dict, Any, Tuple
from tools import calculator_tool, text_analysis_tool, currency_converter_tool

class ReActAgent:
    def __init__(self, llm: Any):
        self.llm = llm
        self.memory: List[Dict[str, str]] = []
        self.available_tools = {
            "calculator": {
                "description": "Evaluates math expressions. Input should be a valid math string e.g., '15 * 850 + 200'",
                "func": calculator_tool
            },
            "text_analyzer": {
                "description": "Calculates word count, character count and stats of input text.",
                "func": text_analysis_tool
            },
            "currency_converter": {
                "description": "Converts USD amount to target currency. Input format: '100 USD to INR'",
                "func": lambda inp: currency_converter_tool(
                    float(inp.split()[0]) if inp.split()[0].replace('.', '', 1).isdigit() else 100,
                    inp.split()[-1] if len(inp.split()) > 1 else "INR"
                )
            }
        }

    def run(self, goal: str, max_steps: int = 5) -> Tuple[str, List[Dict[str, Any]]]:
        """Executes ReAct planning loop (Thought -> Action -> Observation -> Final Answer)."""
        traces = []
        
        system_prompt = f"""You are an Autonomous ReAct AI Agent with Memory and Tools.
Your available tools are:
1. calculator: Evaluates mathematical expressions like '25 * 4'.
2. text_analyzer: Analyzes word count and sentence stats of input text.
3. currency_converter: Converts USD to INR/EUR. Format input like '100 USD to INR'.

To use a tool, output EXACTLY in this format:
Thought: your reasoning step here
Action: tool_name
Action Input: tool input here

When you have the final answer, output:
Thought: I know the final answer now
Final Answer: your final response here

Previous Conversation Memory:
{self._format_memory()}

User Goal: {goal}
"""
        current_prompt = system_prompt
        
        for step in range(1, max_steps + 1):
            response = self.llm.invoke(current_prompt)
            content = response.content.strip()
            
            # Check for Final Answer
            if "Final Answer:" in content:
                thought = content.split("Final Answer:")[0].replace("Thought:", "").strip()
                final_ans = content.split("Final Answer:")[1].strip()
                traces.append({
                    "step": step,
                    "thought": thought,
                    "action": "None (Finished)",
                    "action_input": "N/A",
                    "observation": final_ans
                })
                self.memory.append({"user": goal, "assistant": final_ans})
                return final_ans, traces
            
            # Parse Action & Thought
            thought = "Analyzing next logical step..."
            action = None
            action_input = ""
            
            lines = content.split("\n")
            for line in lines:
                if line.startswith("Thought:"):
                    thought = line.replace("Thought:", "").strip()
                elif line.startswith("Action:"):
                    action = line.replace("Action:", "").strip()
                elif line.startswith("Action Input:"):
                    action_input = line.replace("Action Input:", "").strip()
            
            if action in self.available_tools:
                try:
                    tool_func = self.available_tools[action]["func"]
                    observation = tool_func(action_input)
                except Exception as e:
                    observation = f"Tool execution failed: {str(e)}"
                
                traces.append({
                    "step": step,
                    "thought": thought,
                    "action": action,
                    "action_input": action_input,
                    "observation": observation
                })
                
                current_prompt += f"\n\nThought: {thought}\nAction: {action}\nAction Input: {action_input}\nObservation: {observation}"
            else:
                # Fallback if LLM output direct answer without prefix
                traces.append({
                    "step": step,
                    "thought": thought,
                    "action": "Direct LLM Response",
                    "action_input": "N/A",
                    "observation": content
                })
                self.memory.append({"user": goal, "assistant": content})
                return content, traces
                
        return "Agent reached maximum execution steps.", traces

    def _format_memory(self) -> str:
        if not self.memory:
            return "No previous conversation history."
        return "\n".join([f"User: {m['user']}\nAssistant: {m['assistant']}" for m in self.memory[-3:]])
