# TD3 : agent de réponse à incident

Agent LangChain / deepagents qui traite le ticket INC-2026-0417 à partir des preuves du dossier `incident/`.
Binôme : Clément Vurpillot et Noé Spychala.

## Installation

Python 3.11 ou plus récent est nécessaire (testé sous Debian 13 avec Python 3.13).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Ollama doit tourner avec un compte connecté (modèle cloud). Vérification :

```bash
ollama run nemotron-3-nano:30b-cloud
```

## Traces LangSmith

Compte LangSmith en région EU. À exporter dans le terminal qui lance l'agent (la clé ne doit jamais apparaître dans le code ni dans le dépôt) :

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
export LANGSMITH_API_KEY=
export LANGSMITH_AGENT_ID=td3-vurpillot-spychala
export LANGSMITH_AGENT_ENVIRONMENT=local
export LANGSMITH_PROJECT=td3-vurpillot-spychala
```

## Lancement

Depuis la racine du dépôt, venv activé :

```bash
python agent_v1.py
```

Le script `incident/facture_2024-11.ps1.txt` est une preuve : il ne doit jamais être exécuté.
