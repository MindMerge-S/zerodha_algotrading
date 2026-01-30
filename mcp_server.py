# zerodha_mcp.py
"""
MCP Server for Zerodha Trading Integration
Allows Claude to interact with Zerodha trading platform
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
from core_trading import place_trade, get_quote, get_positions, get_orders
import json

# Initialize MCP server
server = Server("abc-mcp")

@server.list_tools()
async def list_tools():
    """List all available trading tools"""
    return [
        Tool(
            name="natural_trade",
            description="Place Zerodha trade using natural language. Examples: 'buy 10 hdfc', 'sell 5 reliance'",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Natural language trade command (e.g., 'buy 10 hdfc')"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="get_quote",
            description="Get live stock quote with current price, OHLC data, and volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., 'HDFCBANK', 'RELIANCE', 'TCS')"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_positions",
            description="Get current trading positions (both net and day positions)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_orders",
            description="Get order history and status of all orders",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def call_tool(name, arguments):
    """Handle tool execution"""
    
    try:
        if name == "natural_trade":
            command = arguments.get("command", "")
            if not command:
                result = {"error": "Command cannot be empty"}
            else:
                result = place_trade(command)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "get_quote":
            symbol = arguments.get("symbol", "")
            if not symbol:
                result = {"error": "Symbol cannot be empty"}
            else:
                result = get_quote(symbol)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "get_positions":
            result = get_positions()
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "get_orders":
            result = get_orders()
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": f"Tool execution failed: {str(e)}"
            }, indent=2)
        )]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())