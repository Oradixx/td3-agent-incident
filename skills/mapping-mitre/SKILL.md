---
name: mapping-mitre
description: Associer les comportements observés aux techniques MITRE ATT&CK. À utiliser après l'extraction des IOC.
---
1. Pour chaque comportement observé (injection SQL, exécution PowerShell, contournement AMSI, persistance, découverte, C2, exfiltration…), choisir une technique ATT&CK.
2. Appeler check_mitre_id pour chaque ID : écarter un ID inconnu ; si la technique est révoquée ou dépréciée, chercher l'ID actuel et le vérifier à nouveau.
3. Enregistrer la liste dans /output/mitre.json : une entrée par technique avec "id", "nom" (celui renvoyé par check_mitre_id), "tactique" et "preuves" (fichier:ligne).
