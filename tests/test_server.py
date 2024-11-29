from mcp.shared.memory import create_connected_server_and_client_session
from fastmcp.server import FastMCPServer


async def test_list_tools():
    server = FastMCPServer("test_server")
    server.add_tool(lambda x: x)
    async with create_connected_server_and_client_session(
        server._mcp_server
    ) as client_session:
        tools = await client_session.list_tools()
        assert len(tools.tools) == 1


async def test_call_tool():
    server = FastMCPServer("test_server")
    server.add_tool(lambda x: x)
    async with create_connected_server_and_client_session(
        server._mcp_server
    ) as client_session:
        result = await client_session.call_tool("my_tool", {"arg1": "value"})
        assert "error" not in result
        assert len(result.content) > 0
