from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_ollama import ChatOllama

agent = create_deep_agent(
    model=ChatOllama(model="nemotron-3-nano:30b-cloud", temperature=0),
    system_prompt="Tu es un analyste SOC.",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
reponse = agent.invoke({"messages": [{"role": "user",
          "content": "Traite le ticket /incident/ticket_INC-2026-0417.md"}]})
print(reponse["messages"][-1].content)
