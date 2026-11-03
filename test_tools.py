import re
import tempfile
from pathlib import Path

import tools

def titre(nom):
    print(f"\n=== {nom} ===")

titre("verify_ioc")
for ioc in ["203.0.113.42", "192.168.1.100", "malicious-domain.ru", "198.51.100.99"]:
    print(ioc, "->", tools.verify_ioc.invoke(ioc))

titre("decode_powershell_b64")
script = Path("incident/facture_2024-11.ps1.txt").read_text()
encodee = re.search(r'\$encodedCommand = "([^"]+)"', script).group(1)
print(tools.decode_powershell_b64.invoke(encodee))
print(tools.decode_powershell_b64.invoke("pas du base64 !"))

titre("to_utc")
for ts in ["15/Nov/2024:22:14:58 +0100", "2024-11-16T08:42:10Z", "2024-11-16 08:42:10", "hier soir"]:
    print(ts, "->", tools.to_utc.invoke(ts))

titre("check_mitre_id")
for tid in ["T1059.001", "T1190", "T1562.001", "T1086", "T9999"]:
    print(tools.check_mitre_id.invoke(tid))

titre("validate_sigma (règle correcte)")
sigma_ok = """
title: PowerShell lancé par Outlook avec contournement de la politique d'exécution
id: 5f0c7b2e-8a41-4c1e-9d3a-2b6f1e7c9a10
status: experimental
description: Détecte powershell.exe lancé par OUTLOOK.EXE avec -ExecutionPolicy Bypass (INC-2026-0417)
author: Clément Vurpillot, Noé Spychala
date: 2024-11-16
tags:
    - attack.execution
    - attack.t1059.001
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        ParentImage|endswith: '\\OUTLOOK.EXE'
        Image|endswith: '\\powershell.exe'
        CommandLine|contains: '-ExecutionPolicy Bypass'
    condition: selection
level: high
"""
print(tools.validate_sigma.invoke(sigma_ok))

titre("validate_sigma (règle cassée)")
sigma_ko = """
title: Règle incomplète
logsource:
    product: windows
detection:
    selection:
        Image|endswith: '\\powershell.exe'
    condition: selection and filtre
"""
print(tools.validate_sigma.invoke(sigma_ko))

titre("test_yara (règle précise)")
yara_precise = r"""
rule facture_ps1_dropper {
    strings:
        $b64_iex = "SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQA"
        $amsi = "'siIni' + 'tFa'"
        $c2 = "192.168.1.100"
    condition:
        2 of them
}
"""
print(tools.test_yara.invoke(yara_precise))

titre("test_yara (règle trop large)")
yara_large = r"""
rule trop_large {
    strings:
        $wc = "Net.WebClient"
        $wmi = "Get-WmiObject"
    condition:
        any of them
}
"""
print(tools.test_yara.invoke(yara_large))
print(tools.test_yara.invoke("rule cassee { condition: }"))

titre("propose_containment (fichier temporaire, output/ non modifié)")
tools.ACTIONS_FILE = Path(tempfile.mkdtemp()) / "actions_proposees.json"
print(tools.propose_containment.invoke({"action": "bloquer l'IP au pare-feu", "cible": "203.0.113.42",
      "justification": "injections SQL puis connexion admin (web_access.log, app.log:7)"}))
print(tools.ACTIONS_FILE.read_text())
