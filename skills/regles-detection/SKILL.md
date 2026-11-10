---
name: regles-detection
description: Écrire et tester une règle Sigma et une règle YARA. À utiliser après le mapping MITRE.
---
1. Écrire une règle Sigma qui détecte le comportement observé dans les événements EDR (process_creation), avec title, id (UUID), logsource, detection, condition, level et les tags ATT&CK vérifiés.
2. Appeler validate_sigma ; tant que le résultat n'est pas OK, corriger la règle, au plus 3 essais.
3. Écrire une règle YARA sur des chaînes propres au script malveillant (pas des fonctions d'administration courantes).
4. Appeler test_yara ; la règle doit correspondre au script malveillant et à aucun script légitime. Sinon, corriger, au plus 3 essais.
5. Enregistrer les règles dans /output/regle.yml et /output/regle.yar, et noter le dernier résultat de validate_sigma et de test_yara pour le rapport. Après 3 essais sans succès, garder la dernière version et signaler l'échec.
