---
name: confinement
description: Proposer les actions de confinement, sans les exécuter. À utiliser après les règles de détection.
---
1. Déduire des IOC vérifiés et des techniques MITRE les actions utiles (bloquer une IP ou un domaine, désactiver un compte, garder un poste isolé, réinitialiser des mots de passe…).
2. Appeler propose_containment pour chaque action, avec l'action, la cible et une justification qui cite les preuves (fichier:ligne).
3. Ne jamais exécuter une action toi-même : propose_containment l'enregistre pour validation humaine.
