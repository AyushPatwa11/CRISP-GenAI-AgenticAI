import re
from typing import List, Dict, Any, Tuple
from tools import calculator_tool, text_analysis_tool, currency_converter_tool

class ReActAgent:
    def __init__(self, llm: Any):
        self.llm = llm
        self.memory: List[Dict[str, str]] = []
        self.available_tools = {
            "calculator": {
                "description": "Evaluates math expressions. Input example: '1500 * 85 + 450'",
                "func": calculator_tool
            },
            "text_analyzer": {
                "description": "Calculates word count, character count and stats of input text.",
                "func": text_analysis_tool
            },
            "currency_converter": {
                "description": "Converts USD amount to target currency. Input example: '250 USD to INR'",
                "func": lambda inp: currency_converter_tool(
                    float(re.search(r"(\d+(?:\.\d+)?)", inp).group(1)) if re.search(r"(\d+(?:\.\d+)?)", inp) else 100,
                    inp.split()[-1] if len(inp.split()) > 1 else "INR"
                )
            }
        }

    def _format_memory(self) -> str:
        if not self.memory:
            return "None"
        return "\n".join([f"User: {m['user']}\nAgent: {m['assistant']}" for m in self.memory])

    def run(self, goal: str, max_steps: int = 5) -> Tuple[str, List[Dict[str, Any]]]:
        """Executes ReAct planning loop (Thought -> Action -> Observation -> Final Answer)."""
        traces = []
        
        system_prompt = f"""You are an Autonomous ReAct AI Agent with Memory and Tools.
Your available tools are:
1. calculator: Evaluates mathematical expressions like '250 * 86.5 * 1.18'.
2. text_analyzer: Analyzes word count and sentence stats of input text.
3. currency_converter: Converts USD to INR/EUR/GBP. Format input like '250 USD to INR'.

CRITICAL INSTRUCTIONS:
- Execute ONE tool per step.
- Output EXACTLY using these prefixes on separate lines:

Thought: your step-by-step reasoning
Action: tool_name
Action Input: exact input string for the tool

- When you have the final answer after executing tools, output:
Thought: I have calculated the final result
Final Answer: clear explanation of the final answer

User Goal: {goal}
"""
        current_prompt = system_prompt
        
        for step in range(1, max_steps + 1):
            response = self.llm.invoke(current_prompt)
            content = response.content.strip()
            
            # Check for Final Answer
            if "Final Answer:" in content:
                final_parts = content.split("Final Answer:")
                thought = final_parts[0].replace("Thought:", "").strip()
                final_ans = final_parts[1].strip()
                traces.append({
                    "step": step,
                    "thought": thought if thought else "Generated final response based on tool results.",
                    "action": "None (Finished)",
                    "action_input": "N/A",
                    "observation": final_ans
                })
                self.memory.append({"user": goal, "assistant": final_ans})
                return final_ans, traces
            
            # Regex parsing for Thought, Action, Action Input
            thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|$)", content, re.DOTALL)
            action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)", content)
            input_match = re.search(r"Action Input:\s*(.*?)(?=\nThought:|\nAction:|$)", content, re.DOTALL)

            thought = thought_match.group(1).strip() if thought_match else "Reasoning next logical step..."
            action = action_match.group(1).strip() if action_match else None
            action_input = input_match.group(1).strip() if input_match else ""

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
                # If LLM provided direct response without tool action
                traces.append({
                    "step": step,
                    "thought": thought,
                    "action": "Direct Response",
                    "action_input": "N/A",
                    "observation": content
                })
                self.memory.append({"user": goal, "assistant": content})
                return content, traces

        return "Max reasoning steps reached without final answer.", traces
