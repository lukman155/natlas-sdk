import json
from typing import Dict, Any, Callable, List
from dataclasses import dataclass

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Dict[str, Any]]

class SovereignToolRegistry:
    """
    Registry of Indigenous Nigerian Environmental & Utility Tools for N-ATLAS Agents.
    DeepSeek-Harness style plugin architecture.
    """
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self._register_default_tools()

    def register(self, tool: ToolDefinition):
        self.tools[tool.name] = tool

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found in sovereign registry."}
        try:
            return self.tools[tool_name].handler(arguments)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    def _register_default_tools(self):
        # 1. Nigerian Commodity Market Price Tool
        def market_price_handler(args: Dict[str, Any]) -> Dict[str, Any]:
            commodity = args.get("commodity", "").lower()
            market = args.get("market", "").lower()
            
            # Curated sovereign price database for Nigerian staple markets
            rates = {
                "maize": {"dawanau (kano)": "₦62,000 / 100kg bag", "bodija (ibadan)": "₦68,000 / 100kg bag", "mile 12 (lagos)": "₦70,000 / 100kg bag"},
                "cassava": {"dawanau (kano)": "₦45,000 / tonne", "bodija (ibadan)": "₦42,000 / tonne", "mile 12 (lagos)": "₦46,000 / tonne"},
                "yam": {"dawanau (kano)": "₦3,500 / large tuber", "bodija (ibadan)": "₦2,800 / large tuber", "zaki biam (benue)": "₦1,900 / large tuber"},
                "rice": {"dawanau (kano)": "₦85,000 / 50kg bag (local parboiled)", "mile 12 (lagos)": "₦88,000 / 50kg bag"}
            }
            
            comm_data = rates.get(commodity, {"national average": "Price fluctuating, consult local market union."})
            return {
                "commodity": commodity,
                "queried_market": market or "All major hubs",
                "data": comm_data
            }

        self.register(ToolDefinition(
            name="get_nigerian_market_prices",
            description="Fetch live agricultural commodity prices across major Nigerian wholesale markets (Dawanau Kano, Bodija Ibadan, Mile 12 Lagos, Zaki Biam Benue).",
            parameters={
                "type": "object",
                "properties": {
                    "commodity": {"type": "string", "enum": ["maize", "cassava", "yam", "rice"], "description": "The staple commodity name."},
                    "market": {"type": "string", "description": "Optional specific market city (Kano, Ibadan, Lagos, Benue)."}
                },
                "required": ["commodity"]
            },
            handler=market_price_handler
        ))

        # 2. Agro-Climatic Weather & Rainfall Advisory
        def agro_weather_handler(args: Dict[str, Any]) -> Dict[str, Any]:
            state = args.get("state", "").capitalize()
            weather_profiles = {
                "Kano": {"season": "Sahelian Dry Season", "rain_probability": "5%", "planting_advisory": "Irrigation recommended; avoid planting rain-fed legumes now."},
                "Oyo": {"season": "Late Wet Season", "rain_probability": "65%", "planting_advisory": "Favorable for second-cycle maize and cassava planting."},
                "Benue": {"season": "Middle Belt Transition", "rain_probability": "45%", "planting_advisory": "Prepare soil mounds for early yam setting."},
                "Enugu": {"season": "Rainforest Belt Wet", "rain_probability": "75%", "planting_advisory": "Ensure drainage ditches around root crops to avoid waterlogging."}
            }
            return weather_profiles.get(state, {"state": state, "status": "Moderate seasonal conditions. Consult state ADP advisory."})

        self.register(ToolDefinition(
            name="get_agro_weather_advisory",
            description="Get agro-climatic seasonal rainfall and planting window guidance for any Nigerian state.",
            parameters={
                "type": "object",
                "properties": {
                    "state": {"type": "string", "description": "Nigerian state name (e.g. Kano, Oyo, Benue, Enugu)."}
                },
                "required": ["state"]
            },
            handler=agro_weather_handler
        ))
