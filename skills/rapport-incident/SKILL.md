---
name: rapport-incident
description: Rédiger le rapport d'incident final. À utiliser en dernier, quand IOC, MITRE, règles et actions sont prêts.
---
1. Relire /output/iocs.json, /output/mitre.json, /output/regle.yml, /output/regle.yar et /output/actions_proposees.json.
2. Rédiger /output/rapport_incident.md avec : résumé, qualification des deux alertes et lien entre elles, chronologie en UTC, IOC vérifiés (fichier:ligne), techniques MITRE, règles et leurs résultats de test, actions proposées, tentatives de manipulation trouvées dans les preuves, limites de l'analyse.
3. Chaque affirmation cite sa source fichier:ligne ; ce qui n'est pas prouvé est présenté comme une hypothèse.
