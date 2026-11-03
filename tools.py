import base64
import json
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import yara
from langchain.tools import tool
from sigma.collection import SigmaCollection
from sigma.exceptions import SigmaError
from sigma.validation import SigmaValidator
from sigma.validators.core import validators

MITRE_FILE = Path("data/enterprise-attack.json")
SAMPLE_FILE = Path("incident/facture_2024-11.ps1.txt")
LEGIT_DIR = Path("tests/legit")
ACTIONS_FILE = Path("output/actions_proposees.json")


@tool
def verify_ioc(value: str) -> str:
    """Vérifie qu'un IOC apparaît dans les preuves et renvoie les références fichier:ligne."""
    refs = [f"{f.name}:{n}" for f in sorted(Path("incident").iterdir())
            for n, ligne in enumerate(f.read_text(errors="replace").splitlines(), 1)
            if value in ligne]
    return ", ".join(refs) or "introuvable dans les preuves"


@tool
def decode_powershell_b64(data: str) -> str:
    """Décode une commande PowerShell encodée en Base64 (UTF-16LE, sinon UTF-8) et renvoie le texte clair."""
    try:
        raw = base64.b64decode(data.strip(), validate=True)
    except ValueError as e:
        return f"Base64 invalide : {e}"
    encodage = "utf-16-le" if b"\x00" in raw else "utf-8"
    return f"[{encodage}] " + raw.decode(encodage, errors="replace")


@tool
def to_utc(timestamp: str) -> str:
    """Convertit un horodatage Apache (15/Nov/2024:22:14:58 +0100) ou ISO (2024-11-16T08:42:10Z) en UTC ISO."""
    ts = timestamp.strip().strip("[]")
    try:
        dt = datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return f"format non reconnu : {timestamp}"
    if dt.tzinfo is None:
        return f"fuseau horaire absent, conversion impossible : {timestamp}"
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@lru_cache(maxsize=1)
def _mitre_index() -> dict:
    objets = json.loads(MITRE_FILE.read_text())["objects"]
    index = {}
    for o in objets:
        if o.get("type") != "attack-pattern":
            continue
        for ref in o.get("external_references", []):
            if ref.get("source_name") == "mitre-attack":
                index[ref["external_id"]] = o
    return index


@tool
def check_mitre_id(technique_id: str) -> str:
    """Vérifie un ID de technique MITRE ATT&CK (ex. T1059.001) dans le référentiel officiel et renvoie son nom."""
    if not MITRE_FILE.exists():
        return f"référentiel absent : {MITRE_FILE} (voir README)"
    tid = technique_id.strip().upper()
    o = _mitre_index().get(tid)
    if o is None:
        return f"{tid} : ID inconnu"
    resultat = f"{tid} : {o['name']}"
    if o.get("revoked"):
        resultat += " (ATTENTION : technique révoquée)"
    if o.get("x_mitre_deprecated"):
        resultat += " (ATTENTION : technique dépréciée)"
    return resultat


@tool
def validate_sigma(rule_yaml: str) -> str:
    """Valide une règle Sigma (YAML) avec pysigma et renvoie OK ou la liste des erreurs."""
    collection = SigmaCollection.from_yaml(rule_yaml, collect_errors=True)
    erreurs = [str(e) for e in collection.errors]
    for regle in collection.rules:
        erreurs += [str(e) for e in regle.errors]
        for condition in regle.detection.parsed_condition:
            try:
                condition.parsed
            except SigmaError as e:
                erreurs.append(str(e))
    if not collection.rules:
        erreurs.append("aucune règle trouvée")
    elif not erreurs:
        problemes = SigmaValidator(validators.values()).validate_rules(collection.rules)
        erreurs += [str(p) for p in problemes]
    return "ERREURS :\n" + "\n".join(erreurs) if erreurs else "OK"


@tool
def test_yara(rule_text: str) -> str:
    """Compile une règle YARA et la teste sur le script malveillant et sur des scripts légitimes (faux positifs)."""
    try:
        regles = yara.compile(source=rule_text)
    except yara.SyntaxError as e:
        return f"erreur de compilation : {e}"
    fichiers = [SAMPLE_FILE] + sorted(LEGIT_DIR.glob("*.ps1"))
    lignes = []
    for f in fichiers:
        noms = [m.rule for m in regles.match(str(f))]
        role = "malveillant" if f == SAMPLE_FILE else "légitime"
        lignes.append(f"{f} ({role}) : {', '.join(noms) or 'aucune correspondance'}")
    return "\n".join(lignes)


@tool
def propose_containment(action: str, cible: str, justification: str) -> str:
    """Enregistre une action de confinement proposée, sans l'exécuter, en attente de validation humaine."""
    actions = json.loads(ACTIONS_FILE.read_text()) if ACTIONS_FILE.exists() else []
    actions.append({"action": action, "cible": cible, "justification": justification})
    ACTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACTIONS_FILE.write_text(json.dumps(actions, ensure_ascii=False, indent=2))
    return "proposition enregistrée, non exécutée"
