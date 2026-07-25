from typing import Dict, Any, List
from external_tools import get_live_weather, search_web_duckduckgo, create_calendar_invite_mock

class MCPToolRegistry:
    """Implements Model Context Protocol (MCP) standardized tool schemas."""
    
    def __init__(self):
        self.tools = {
            "get_live_weather": {
                "name": "get_live_weather",
                "description": "Fetches current real-time weather temperature and wind speed for any city worldwide.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "Name of the target city (e.g. Bhilai, Delhi, London)"
                        }
                    },
                    "required": ["city"]
                },
                "executor": get_live_weather
            },
            "search_web": {
                "name": "search_web",
                "description": "Searches the live web for recent news, articles, and real-time information.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query string"
                        }
                    },
                    "required": ["query"]
                },
                "executor": search_web_duckduckgo
            },
            "create_calendar_invite": {
                "name": "create_calendar_invite",
                "description": "Schedules a new calendar event with specified title, date, and attendee emails.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Title of the meeting"},
                        "date_str": {"type": "string", "description": "Date & time (e.g., 2026-07-26 14:00)"},
                        "attendees": {"type": "string", "description": "Comma separated attendee emails"}
                    },
                    "required": ["title", "date_str", "attendees"]
                },
                "executor": lambda params: create_calendar_invite_mock(
                    params.get("title", "Meeting"),
                    params.get("date_str", "Tomorrow"),
                    params.get("attendees", "")
                )
            }
        }

    def list_mcp_schemas(self) -> List[Dict[str, Any]]:
        """Returns standard MCP-compliant JSON schema definitions."""
        return [
            {
                "name": meta["name"],
                "description": meta["description"],
                "inputSchema": meta["inputSchema"]
            }
            for meta in self.tools.values()
        ]

    def execute_mcp_call(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Executes a tool call using standard MCP parameters."""
        if tool_name not in self.tools:
            return f"MCP Error: Tool '{tool_name}' not registered in MCP Server."
        
        executor = self.tools[tool_name]["executor"]
        if tool_name == "get_live_weather":
            return executor(arguments.get("city", "Bhilai"))
        elif tool_name == "search_web":
            return executor(arguments.get("query", ""))
        else:
            return executor(arguments)
