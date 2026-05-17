import { create } from 'zustand'

// Graphe vide par défaut (sera remplacé par le cas TechNova au lancement)
const emptyGraph = {
  macro_nodes: [],
  macro_edges: [],
  meso_nodes: [],
  meso_edges: [],
  micro_nodes: [],
  micro_edges: [],
  memberships_macro_meso: [],
  memberships_meso_micro: [],
}

export const useGraphStore = create((set, get) => ({
  // ---------- État ----------
  graph: emptyGraph,
  diagnosis: null,
  isLoading: false,
  error: null,

  // ---------- Mutations sur le graphe ----------
  setGraph: (graph) => set({ graph }),

  addNode: (level, node) => set((state) => {
    const key = `${level}_nodes`
    return { graph: { ...state.graph, [key]: [...state.graph[key], node] } }
  }),

  removeNode: (level, nodeId) => set((state) => {
    const nKey = `${level}_nodes`
    const eKey = `${level}_edges`
    return {
      graph: {
        ...state.graph,
        [nKey]: state.graph[nKey].filter(n => n.id !== nodeId),
        [eKey]: state.graph[eKey].filter(e => e.source !== nodeId && e.target !== nodeId),
      },
    }
  }),

  updateNodePosition: (level, nodeId, x, y) => set((state) => {
    const key = `${level}_nodes`
    return {
      graph: {
        ...state.graph,
        [key]: state.graph[key].map(n => (n.id === nodeId ? { ...n, x, y } : n)),
      },
    }
  }),

  addEdge: (level, edge) => set((state) => {
    const key = `${level}_edges`
    return { graph: { ...state.graph, [key]: [...state.graph[key], edge] } }
  }),

  removeEdge: (level, edgeId) => set((state) => {
    const key = `${level}_edges`
    return {
      graph: { ...state.graph, [key]: state.graph[key].filter(e => e.id !== edgeId) },
    }
  }),

  // Ajoute un bloc Lego entier (en remappant les IDs pour éviter les collisions)
  insertBlock: (block, idSuffix = '') => set((state) => {
    const suffix = idSuffix || `_${Date.now()}`
    const remap = (id) => `${id}${suffix}`
    const level = block.level
    const nKey = `${level}_nodes`
    const eKey = `${level}_edges`

    const newNodes = block.nodes.map(n => ({
      id: remap(n.id),
      label: n.label,
      level,
      type: n.type || 'default',
      capacity: n.capacity ?? 1.0,
      cost: n.cost ?? 0.0,
      performance: 1.0,
      workload: 0.5,
      x: 0,
      y: 0,
    }))

    const newEdges = block.edges.map((e, i) => ({
      id: `e_${suffix}_${i}`,
      source: remap(e.source),
      target: remap(e.target),
      type: e.type || 'hierarchy',
      weight: e.weight ?? 1.0,
      frequency: e.weight ?? 1.0,
    }))

    return {
      graph: {
        ...state.graph,
        [nKey]: [...state.graph[nKey], ...newNodes],
        [eKey]: [...state.graph[eKey], ...newEdges],
      },
    }
  }),

  // ---------- Diagnostic ----------
  setDiagnosis: (diagnosis) => set({ diagnosis }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}))
