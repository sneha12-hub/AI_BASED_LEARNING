from langchain.tools import __all__ as all_tools

print("List of Built-in Tools in LangChain:")
for tool in all_tools:
    print(f"- {tool}")
