# OrgaLego

> Simulateur 2D interactif pour la conception et le diagnostic de structures organisationnelles, basé sur les grandes écoles de pensée (Mintzberg, Fayol, Weber...).

OrgaLego permet de modéliser une organisation comme un graphe hiérarchique à trois niveaux (macro, méso, micro), d'assembler des "blocs Lego" représentant des archétypes théoriques, et d'obtenir un diagnostic en temps réel via trois algorithmes de théorie des graphes :

- **Louvain** : détection des silos
- **Centralité d'intermédiarité** : identification des goulots
- **Matching d'archétypes** : comparaison à la typologie de Mintzberg

## Architecture

```
orgalego/
├── backend/    # API Python (FastAPI + NetworkX)
├── frontend/   # Interface React 2D (React Flow + Zustand)
├── shared/     # Exemples partagés (cas TechNova)
└── docs/       # Documentation et spécifications LaTeX
```

## Lancer le projet en local

### Prérequis

- Python 3.11+
- Node.js 20+
- npm

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate         # Linux/macOS
# .venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

L'API est accessible sur http://localhost:8000 et la documentation interactive sur http://localhost:8000/docs.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

L'application est accessible sur http://localhost:5173.

## Tester

```bash
cd backend
pytest
```

## Périmètre MVP

- Backend complet avec les 3 algorithmes (Louvain, betweenness, archétypes)
- Frontend 2D avec navigation par clic entre les 3 niveaux
- Bibliothèque initiale de 6 à 8 blocs Lego (configurations de Mintzberg)
- WebSocket pour le diagnostic en temps réel

## Extensions prévues (si le temps le permet)

1. **Algorithmes d'optimisation** : PageRank (leaders informels), recuit simulé (optimisation automatique)
2. **Vue 3D** : représentation tridimensionnelle des trois niveaux empilés (React Three Fiber)

## Licence

MIT
