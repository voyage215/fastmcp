# Project Structure Report

This document outlines the structure of the project, detailing the purpose of its main directories.

## Main Directories

The project is organized into several key directories, each serving a distinct role in the development and maintenance of the software.

### `src`

The `src` directory is the heart of the project, containing all the core source code. This is where the primary logic and implementation of the application reside. In Python projects, this directory typically houses the main Python packages and modules that make up the application.

### `examples`

The `examples` directory provides usage demonstrations of the project. It contains scripts and code snippets that showcase how to use the functionalities implemented in the `src` directory. This is helpful for users and developers to quickly understand and utilize the project's features. The examples might range from simple use cases to more complex scenarios.

### `tests`

The `tests` directory is dedicated to housing all testing-related code. This includes unit tests, integration tests, and potentially end-to-end tests. The purpose of this directory is to ensure the reliability, correctness, and stability of the codebase. Automated tests are run from here to verify that changes to the code do not introduce regressions and that new features work as expected.

### `docs`

The `docs` directory contains all project documentation. This can include API documentation, user guides, tutorials, design documents, and other relevant information that helps in understanding, using, and contributing to the project. Well-maintained documentation is crucial for making the project accessible and maintainable.

## `src/fastmcp` Directory Deep Dive

The `src/fastmcp` directory contains the core implementation of the FastMCP (Fast Model Control Plane) framework. This framework is designed to facilitate interactions with language models by providing a structured way to define tools, manage resources, and handle communication between a client and a server.

### Core Components:

#### 1. Server (`server.py`)

The `server.py` file defines the `FastMCP` class, which is the central component of the server-side framework. Its key responsibilities and features include:
*   **Tool Management**: Integrating and exposing tools (functions or capabilities) that a language model can invoke.
*   **Resource Management**: Handling resources (data or services) that tools might need to operate.
*   **Prompt Management**: Storing and managing prompts that are used to instruct the language model.
*   **Context Handling**: Managing the conversational context and state for interactions with the model.
*   The server listens for requests from clients, processes them by potentially invoking tools or generating model responses, and sends back the results.

#### 2. Client (`client.py`)

The `client.py` file implements the `Client` class, which acts as the interface for applications to interact with a FastMCP server. Its main functionalities are:
*   **Sending Requests**: Formulating and sending requests to the server, which might include user queries or instructions for the language model.
*   **Receiving Responses**: Handling responses from the server, which could be model-generated text, tool invocation results, or errors.
*   **Communication Abstraction**: It abstracts the underlying communication mechanism (transports) from the application logic.

#### 3. Managers

To keep the server organized and modular, FastMCP uses several manager classes:
*   **`ToolManager` (`tools/tool_manager.py`)**: This class is responsible for discovering, registering, and managing the lifecycle of tools available to the FastMCP server. It allows the server to dynamically add or remove capabilities.
*   **`ResourceManager` (`resources/resource_manager.py`)**: This class handles the loading, storage, and access of resources. Tools can request resources through this manager, ensuring that data is handled consistently.
*   **`PromptManager` (`prompts/prompt_manager.py`)**: This class is dedicated to managing prompts. It allows for storing, retrieving, and potentially versioning different prompts used in interactions with the language model.

#### 4. Transports (`client/transports.py`)

Transports are responsible for the actual communication layer between the `Client` and the `FastMCP` server. The `client/transports.py` module likely defines different mechanisms (e.g., HTTP, WebSockets) through which the client and server can exchange messages. This design allows FastMCP to be flexible and adaptable to different communication protocols and deployment scenarios.

#### 5. CLI (`cli` subdirectory)

The `cli` subdirectory contains the code for the FastMCP command-line interface. This interface provides users and developers with command-line tools to:
*   Start and manage the FastMCP server.
*   Interact with the server (e.g., send test queries).
*   Potentially configure server settings or inspect its state.
*   Facilitate development and debugging tasks.

The FastMCP framework, through these components, aims to provide a robust and extensible platform for building applications powered by language models.

## Entry Points for Understanding the Code

For junior developers looking to understand the FastMCP codebase, the following files and directories are recommended as starting points:

1.  **`README.md`**: Always start with the main `README.md` file at the project root. It provides a high-level overview of the project, its purpose, installation instructions, and often, basic usage examples.

2.  **`examples/simple_echo.py`**: The `examples` directory contains practical demonstrations. `simple_echo.py` is likely a good starting point to see a minimal working example of a client-server interaction using FastMCP. Understanding how an example works can provide a concrete foundation before diving into the framework's internals.

3.  **`src/fastmcp/__init__.py`**: This file is the entry point for the `fastmcp` package. It often defines what classes and functions are publicly exposed by the package, giving an idea of the main interfaces.

4.  **`src/fastmcp/server/server.py`**: As detailed earlier, this file contains the `FastMCP` class, which is the core of the server-side logic. Understanding this class is crucial to grasping how the server operates, manages tools, resources, and handles client requests.

5.  **`src/fastmcp/client/client.py`**: This file defines the `Client` class, which is the primary interface for applications to communicate with the FastMCP server. Examining this file will help in understanding how to send requests to the server and process its responses.

By starting with these files, a developer can gradually build an understanding of the project's architecture and how its different components interact. After grasping these core elements, exploring the manager classes (`ToolManager`, `ResourceManager`, `PromptManager`) and the `transports` module would be logical next steps.

## Key Concepts

This section highlights important concepts within the FastMCP framework.

### 1. MCP (Model Context Protocol)

**Explanation:** The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) is a standardized way to provide context and tools to Language Models (LLMs). It defines how LLM applications can interact with servers that expose data (Resources) and functionality (Tools). FastMCP is a Pythonic implementation of this protocol, simplifying the creation of MCP-compliant servers and clients.

### 2. Tools

**Explanation:** Tools are Python functions (synchronous or asynchronous) that LLMs can execute to perform actions. These are ideal for computations, API calls, or any side effects (like database operations). FastMCP automatically generates the necessary schema for these tools from type hints and docstrings, making them discoverable and usable by the LLM.

**Code Snippet (from `examples/simple_echo.py`):**
```python
from fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")

@mcp.tool()
def echo(text: str) -> str:
    """Echo the input text"""
    return text
```

### 3. Resources

**Explanation:** Resources expose read-only data sources to the LLM, similar to how a `GET` request works in a traditional web API. They are defined by decorating a function with `@mcp.resource("your://uri")`. Resources can also be dynamic templates by including placeholders in the URI (e.g., `users://{user_id}/profile`), allowing clients to request specific subsets of data.

**Code Snippet (from `README.md`):**
```python
# Static resource
@mcp.resource("config://version")
def get_version():
    return "2.0.1"

# Dynamic resource template
@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    # Fetch profile for user_id...
    return {"name": f"User {user_id}", "status": "active"}
```

### 4. Prompts

**Explanation:** Prompts are reusable message templates that guide LLM interactions. In FastMCP, you define prompts by decorating functions with `@mcp.prompt()`. These functions can return strings or `Message` objects, providing a structured way to instruct the LLM for specific tasks.

**Code Snippet (from `README.md`):**
```python
@mcp.prompt()
def summarize_request(text: str) -> str:
    """Generate a prompt asking for a summary."""
    return f"Please summarize the following text:\n\n{text}"
```

### 5. Context (`ctx`)

**Explanation:** The `Context` object (`ctx`) provides access to MCP session capabilities within your tools, resources, or prompts. By adding a parameter annotated as `Context` (e.g., `ctx: Context`) to an MCP-decorated function, FastMCP injects the context object. This allows functions to perform operations like logging messages to the client (`ctx.info()`), requesting LLM completions from the client (`ctx.sample()`), making HTTP requests (`ctx.http_request()`), reading other resources (`ctx.read_resource()`), and reporting progress (`ctx.report_progress()`).

**Code Snippet (from `README.md`):**
```python
from fastmcp import FastMCP, Context

mcp = FastMCP("My MCP Server")

@mcp.tool()
async def process_data(uri: str, ctx: Context):
    # Log a message to the client
    await ctx.info(f"Processing {uri}...")

    # Read a resource from the server
    data = await ctx.read_resource(uri)

    # Ask client LLM to summarize the data
    summary = await ctx.sample(f"Summarize: {data.content[:500]}")

    # Return the summary
    return summary.text
```

### 6. Client-Server Interaction

**Explanation:** FastMCP facilitates communication between a `Client` and a `FastMCP` server. The client sends requests (e.g., to call a tool or read a resource) to the server. The server processes these requests, potentially executing a tool function or retrieving resource data, and then sends a response back to the client. FastMCP supports various transport mechanisms (like Stdio, HTTP) for this interaction. The `fastmcp.Client` class allows programmatic interaction with any MCP server.

**Code Snippet (Conceptual Client Usage - from `README.md`):**
```python
from fastmcp import Client

async def main():
    # Connect via stdio to a local script (server)
    async with Client("my_server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("add", {"a": 5, "b": 3}) # Assuming 'add' tool exists on server
        print(f"Result: {result.text}")

# To run this client example, you would need a 'my_server.py' with an 'add' tool:
# # my_server.py
# from fastmcp import FastMCP
# mcp_server = FastMCP("MyServer")
# @mcp_server.tool()
# def add(a: int, b: int) -> int: return a + b
# if __name__ == "__main__": mcp_server.run()
```
