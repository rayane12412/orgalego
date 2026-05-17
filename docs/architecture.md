# Architecture d'OrgaLego

Document interne destiné aux développeurs du projet.

## Vue d'ensemble

OrgaLego suit une architecture client-serveur classique :

```
┌─────────────────────────────┐         WebSocket          ┌──────────────────────────┐
│  Frontend React + ReactFlow │  ───── /ws/graph ─────►   │  Backend FastAPI Python  │
│  (port 5173)                │  ◄── diagnosis_result ──   │  (port 8000)             │
└─────────────────────────────┘                            └──────────────────────────┘
                                                                    │
                                                                    ▼
                                                          NetworkX + python-louvain
                                                          SQLite (projets utilisateur)
                                                          JSON statiques (blocs Lego)
```

## Flux d'une interaction utilisateur

1. L'utilisateur ajoute un bloc Lego ou déplace un nœud dans `GraphView`.
2. `graphStore` (Zustand) met à jour l'état local.
3. `useOrgaLegoSocket` détecte le changement et envoie un message `graph_update` via WebSocket (debounced à 200 ms).
4. Côté backend, `websocket_graph.py` valide le payload via Pydantic et délègue à `core.diagnosis.run_full_diagnosis`.
5. L'orchestrateur appelle successivement les 3 algorithmes (Louvain, betweenness, archétypes) sur le sous-graphe en focus.
6. Le résultat est sérialisé et renvoyé sur le WebSocket.
7. `useOrgaLegoSocket` reçoit le message, met `diagnosis` dans le store, ce qui déclenche le re-rendu de `GraphView` (couleurs des nœuds) et `DiagnosisPanel`.

## Niveaux hiérarchiques

Trois niveaux empilés représentent l'organisation :

- **Macro** : divisions, business units (~5-20 nœuds)
- **Méso** : équipes, comités (~10-50 nœuds)
- **Micro** : individus (~50-500 nœuds)

Reliés par des arêtes inter-niveaux dites de **membership** (un humain peut appartenir à plusieurs équipes avec une pondération).

## Navigation par clic

L'utilisateur ne voit qu'un seul niveau à la fois :
- Vue macro globale par défaut
- Clic sur une division → vue méso filtrée sur cette division
- Clic sur une équipe → vue micro filtrée sur cette équipe
- Le `Breadcrumb` permet de remonter à n'importe quel niveau

Le filtrage par parent est géré dans `core/graph_builder.py` côté backend et dans `GraphView.jsx` côté frontend.

## Schémas Pydantic = contrat d'interface

Les fichiers `backend/app/schemas/*.py` sont la source de vérité. Toute modification doit être répercutée côté frontend dans les payloads attendus. Voir notamment :
- `block.py` : Block, BlockNode, BlockEdge, BlockLevel
- `graph.py` : FullGraph, GraphNode, GraphEdge, MembershipEdge, GraphUpdate
- `diagnosis.py` : Diagnosis, NodeMetrics, CommunityResult, ArchetypeMatch, Recommendation
- `project.py` : Project, ProjectCreate, ProjectUpdate

## Algorithmes du MVP

| Algorithme | Module | Question organisationnelle |
|---|---|---|
| Louvain | `core/algorithms/communities.py` | Y a-t-il des silos ? |
| Centralité d'intermédiarité | `core/algorithms/centrality.py` | Quels sont les goulots ? |
| Matching d'archétypes | `core/algorithms/archetypes.py` | À quelle configuration de Mintzberg correspond la structure ? |

PageRank et recuit simulé sont prévus pour les versions ultérieures (v2/v3).

## Extension : ajouter un nouveau bloc Lego

1. Créer un JSON dans `backend/app/blocks/levelN_xxx/mon_bloc.json` (suivre le schéma `Block`).
2. Redémarrer le backend (le cache se reconstruit au démarrage).
3. Le bloc apparaît automatiquement dans la palette frontend.

## Extension : ajouter un nouvel algorithme

1. Créer `backend/app/core/algorithms/mon_algo.py` exposant une fonction pure `f(g: nx.Graph) -> Result`.
2. Ajouter un schéma Pydantic dans `schemas/diagnosis.py` pour le résultat.
3. Appeler la fonction dans `core/diagnosis.py` et l'ajouter à l'objet `Diagnosis` retourné.
4. Côté frontend, ajouter une `MetricCard` dans `DiagnosisPanel`.

## Tests

```bash
cd backend
pytest                # tous les tests
pytest tests/test_algorithms.py -v   # seuls les algos
```

## Lancer en dev

Deux terminaux :

```bash
# Terminal 1 - backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2 - frontend
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:5173.

## Limites assumées du MVP

- Pas d'authentification utilisateur (single-user local)
- Pas de gestion de versions de graphes
- Pas d'import depuis Excel/CSV (prévu en v2)
- Layout 2D simpliste (circulaire ou en grille) — pas de force-directed automatique
- Les diagnostics sont **indicatifs**, pas prédictifs : ils décrivent l'état actuel, pas l'évolution future
