import { create } from 'zustand'

// Le fil d'Ariane est une pile de niveaux visités.
// Niveau initial : macro (sans parent).
// Quand l'utilisateur clique sur un nœud macro, on empile { level: 'meso', parent: nodeId, parentLabel }.
// Quand il clique sur un nœud méso, on empile { level: 'micro', parent: nodeId, parentLabel }.

const ROOT = { level: 'macro', parent: null, parentLabel: 'Organisation' }

export const useNavigationStore = create((set, get) => ({
  path: [ROOT],

  current: () => {
    const path = get().path
    return path[path.length - 1]
  },

  drillDown: (level, parentId, parentLabel) => set((state) => ({
    path: [...state.path, { level, parent: parentId, parentLabel }],
  })),

  goTo: (index) => set((state) => ({
    path: state.path.slice(0, index + 1),
  })),

  goUp: () => set((state) => ({
    path: state.path.length > 1 ? state.path.slice(0, -1) : state.path,
  })),

  reset: () => set({ path: [ROOT] }),
}))
