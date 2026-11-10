from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_ollama import ChatOllama

from tools import (check_mitre_id, decode_powershell_b64, propose_containment, test_yara,
                   to_utc, validate_sigma, verify_ioc)

agent = create_deep_agent(
    model=ChatOllama(model="nemotron-3-nano:30b-cloud", temperature=0),
    system_prompt=Path("prompts/system_prompt.md").read_text(),
    tools=[verify_ioc, decode_powershell_b64, to_utc, check_mitre_id,
           validate_sigma, test_yara, propose_containment],
    skills=["/skills/"],
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
reponse = agent.invoke({"messages": [{"role": "user",
          "content": "Traite le ticket /incident/ticket_INC-2026-0417.md"}]})
print(reponse["messages"][-1].content)
