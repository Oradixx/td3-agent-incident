---
name: extraction-ioc
description: Extraire et vérifier les IOC. À utiliser pour lister les IOC (IP, domaines, URL, hash, chemins, comptes) des preuves.
---
1. Relever les indicateurs dans chaque preuve de /incident/ (lue en entier).
2. Décoder avec decode_powershell_b64 toute commande PowerShell encodée, et relever les indicateurs du texte décodé.
3. Appeler verify_ioc pour chacun, et écarter ceux qui sont introuvables.
4. Enregistrer la liste dans /output/iocs.json : une entrée par IOC avec "type", "valeur", "references" (les fichier:ligne renvoyés par verify_ioc) et "contexte" (une phrase).
