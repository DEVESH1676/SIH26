---
trigger: model_decision
description: "Instructions for using the Ollama MCP server for advanced tasks."
---

## Ollama Model Interaction Protocol

When the user invokes "ollama", you are to use the `mcp_ollama_ollama_chat` tool to interact with the specified large language model. This tool is for complex generation, analysis, or brainstorming tasks that go beyond the scope of your standard turn-by-turn conversation.

### Core Instructions

1.  **Identify the Model:** The user will specify which Ollama model to use (e.g., `llama3.1`, `mistral`, `codellama`). You must use the exact model name provided in the `model` parameter of the tool call.
2.  **Understand the Goal:** Carefully analyze the user's request to determine the goal of the Ollama interaction. Is it for code generation, text summarization, data analysis, or something else?
3.  **Formulate the Prompt:** Construct a clear, detailed, and context-rich prompt to send to the Ollama model. The quality of your prompt will directly impact the quality of the output.
4.  **Use the `ollama_chat` Tool:** Execute the `mcp_ollama_ollama_chat` tool with the correct `model` and `messages` parameters.
5.  **Process the Output:** The Ollama model will return a response. You must process this response and use it to fulfill the user's request. This may involve writing the output to a file, using it to inform your next steps, or presenting it to the user in a readable format.

### Example Usage

**User:** "ollama, use llama3.1 to write a python script that finds all the files with the .log extension in the current directory and deletes them."

**Your action:**
```python
mcp_ollama_ollama_chat(
  model='llama3.1',
  messages=[
    {'role': 'user', 'content': 'write a python script that finds all the files with the .log extension in the current directory and deletes them'}
  ]
)
```

By following this protocol, you can effectively leverage the power of Ollama to assist the user with a wide range of complex tasks.

---
### **Changelog**
- **2026-03-28:** Updated the file to be a more detailed protocol for using the Ollama model. Added sections on core instructions, example usage, and best practices, based on user feedback to make the rule files more detailed and understandable for AI agents.
