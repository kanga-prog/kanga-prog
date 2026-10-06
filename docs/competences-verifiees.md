# Compétences vérifiées — sources et limites

Ce document distingue les éléments observés dans les dépôts locaux, les contributions Git attribuables et les informations fournies dans le brief/CV. Il ne transforme ni une dépendance, ni un répertoire vide, ni une réalisation collective non attribuée en compétence démontrée.

## Règles de lecture

- **Preuve de dépôt** : fichiers d'exercice, code, README ou historique Git consultés localement.
- **Contribution personnelle** : commit(s) locaux attribués à `kanga-prog` ou à Brice Kanga.
- **Brief/CV** : information fournie pour ce profil, à ne pas présenter comme résultat de production sans autre preuve.
- Les tests et simulations de sécurité décrits ci-dessous restent cantonnés à des environnements autorisés.

## Inventaire fondé sur les dépôts

| Matière / expérience | Exercice, lab ou projet observé | Outils / technologies observés | Preuve consultée | Formulation utilisable dans le profil |
| --- | --- | --- | --- | --- |
| Réseaux | `holbertonschool-network` : OSI, TCP/UDP, ports, écoute locale et parcours DNS/HTTPS lors d'une requête Web. | TCP/IP, DNS, ports, HTTP/HTTPS. | `basics_0`, `basics_1` et `what_happens_when_your_type_google_com_in_your_browser_and_press_enter`, avec README et scripts. | « Formation pratique aux fondamentaux réseau : TCP/IP, DNS, ports et cheminement d'une requête Web. » |
| Backend JavaScript | `holbertonschool-web_back_end` : ES6, promesses, Node.js, Express, pagination. | JavaScript, Node.js, Express, Babel, Jest, ESLint, Python. | Exercices et README dans `ES6_*`, `Node_JS_basic`, `pagination`, `python_async_*` et `python_variable_annotations`. | « Exercices fullstack/back-end : Node.js/Express, JavaScript asynchrone, pagination REST et Python typé/asynchrone. » |
| Données | Projet NoSQL de formation. | MongoDB, PyMongo, opérations CRUD et agrégation. | `holbertonschool-web_back_end/NoSQL` contient le README et les scripts demandés. | « Pratique de MongoDB/PyMongo : requêtes, opérations CRUD et agrégations. » |
| Frontend typé | Exercices TypeScript Holberton. | TypeScript. | `holbertonschool-web_react/TypeScript` avec tâches et sources TypeScript. | « Exercices TypeScript dans le parcours frontend. » |
| Détection / Purple Team | PurpleWatch : règles Wazuh versionnées et preuves de validation de scénarios contrôlés. | Caldera, Sandcat, auditd, Wazuh, MITRE ATT&CK, `wazuh-analysisd`, `wazuh-logtest`. | `README.md`, `detections/wazuh/`, `docs/evidence/`, `docs/runbooks/` et historique Git local de PurpleWatch. | « Validation en laboratoire autorisé de la chaîne Caldera → auditd → Wazuh ; écriture/documentation de règles et analyse d'alertes. » |
| Développement sécurisé | WatYouFace : authentification, JWT, rôles et endpoints protégés. | Java 17, Spring Boot, Spring Security, JWT, PostgreSQL, WebSocket, React. | `pom.xml`, `SecurityConfig`, `JwtAuthenticationFilter`, `Authz`, `WebSocketConfig` et commits locaux attribués à `kanga-prog`. | « Développement d'une application Spring sécurisée par JWT et contrôle de rôles, avec frontend React. » |
| Projet collaboratif | Rebois-Connect : début et itérations frontend historiques. | React, Tailwind CSS, Flask, Docker, formulaire et routage protégé. | Historique Git local : cinq commits attribués à `kanga-prog`, notamment sur `frontend-bis`; le code actuel contient aussi des changements locaux collectifs. | « Contribution frontend à un projet collaboratif React ; périmètre individuel limité aux fichiers présents dans l'historique personnel. » |
| Conception produit | Bagage Voyage. | Parcours utilisateur, cahier des charges, priorisation et documentation. | Arborescence locale de documents de conception ; aucun état de code versionné exploitable n'a été confirmé lors de l'audit. | « Conception d'un service de logistique bagages : parcours, règles métier et documentation. » |

## Contributions PurpleWatch attribuables

L'historique local comporte des commits attribués à Brice Kanga et à `kanga-prog` sur les règles de détection, les runbooks, les preuves de validation, la livraison finale et les fondations de l'API FastAPI. La présentation publique reste volontairement collective :

- contribution explicitement valorisable : validation Linux Caldera → auditd → Wazuh, règles `execve`, collecte/corrélation des événements et passation ;
- éléments d'équipe : architecture globale, couverture Windows, métriques et backend FastAPI ; ils ne sont pas présentés comme des réalisations individuelles sans citer la contribution correspondante ;
- les résultats de planification (P50/P95, taux de détection, corrélations temporelles et techniques MITRE additionnelles) ne sont pas repris comme acquis sans preuve de validation clairement associée.

## Éléments issus du brief/CV à confirmer avant de les renforcer

Les éléments suivants peuvent rester dans une section « formation et labs » du profil, avec un vocabulaire prudent. Aucun n'est présenté ici comme une maîtrise experte ou un résultat de production tant qu'une preuve complémentaire n'est pas associée :

- OWASP Top 10, IDOR/BOLA, SSRF, injections de commandes et LFI/RFI ;
- Burp Suite, Nmap, Nessus, Metasploit et Postman ;
- sécurité mobile : Base64/XOR, dérivation de clé et analyse JADX ;
- MySQL, Next.js, Hono, Kysely, Stripe, Vitest, Redis distribué et les évolutions de paiement Bagage Voyage ;
- chiffres de tests, métriques de détection, scalabilité multi-instance et statuts précis des exigences PAY-04/PAY-06.

## Publication et liens

- Les remotes locaux identifient les dépôts attendus, mais l'accès GitHub/API disponible lors de l'audit ne permettait pas de confirmer leur visibilité publique. Les lignes « À confirmer » du README ne doivent pas être remplacées par une URL avant vérification manuelle.
- Bagage Voyage doit rester une présentation publique limitée : description, architecture expurgée et captures anonymisées uniquement. Aucun code privé, document administratif, donnée client, secret, IP de lab ou lien privé ne doit être publié.
- Dépôts candidats à épingler après vérification de visibilité et nettoyage : PurpleWatch (détection), WatYouFace backend + frontend (fullstack sécurisé), `holbertonschool-cyber_security` lorsqu'il contient des labs publiables, et un dépôt Bagage Voyage expurgé distinct si nécessaire.

## Descriptions et topics proposés (après vérification du contenu et de la visibilité)

| Dépôt | Description proposée | Topics proposés |
| --- | --- | --- |
| PurpleWatch | « Laboratoire Purple Team autorisé : détection Wazuh, télémétrie auditd/Sysmon et scénarios MITRE ATT&CK contrôlés. » | `cybersecurity`, `purple-team`, `wazuh`, `mitre-attack`, `detection-engineering`, `auditd` |
| WatYouFace backend | « API Spring Boot pour plateforme sociale : JWT, rôles, endpoints protégés et WebSocket. » | `java`, `spring-boot`, `spring-security`, `jwt`, `postgresql`, `websocket` |
| WatYouFace frontend | « Frontend React de plateforme sociale, connecté à une API sécurisée. » | `react`, `vite`, `javascript`, `frontend` |
| Rebois-Connect | « Projet collaboratif React/Flask pour services environnementaux et fonciers. » | `react`, `flask`, `tailwindcss`, `docker`, `collaborative-project` |
