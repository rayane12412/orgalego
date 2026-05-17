// Mise en page 2D simple : disposition circulaire / en cluster

const RADIUS = 220
const CENTER = { x: 400, y: 300 }

// Disposition circulaire pour un ensemble de nœuds
export function circularLayout(nodes, center = CENTER, radius = RADIUS) {
  if (nodes.length === 0) return []
  if (nodes.length === 1) return [{ ...nodes[0], x: center.x, y: center.y }]
  return nodes.map((n, i) => {
    const angle = (2 * Math.PI * i) / nodes.length
    return {
      ...n,
      x: center.x + radius * Math.cos(angle),
      y: center.y + radius * Math.sin(angle),
    }
  })
}

// Disposition en grille (utile pour les vues micro avec beaucoup de nœuds)
export function gridLayout(nodes, cols = 4, spacing = 150, origin = { x: 100, y: 100 }) {
  return nodes.map((n, i) => ({
    ...n,
    x: origin.x + (i % cols) * spacing,
    y: origin.y + Math.floor(i / cols) * spacing,
  }))
}

// Choisit automatiquement une mise en page selon le nombre de nœuds
export function autoLayout(nodes) {
  if (nodes.length <= 8) return circularLayout(nodes)
  return gridLayout(nodes)
}

// Applique le layout uniquement si les positions ne sont pas déjà définies
export function ensurePositions(nodes) {
  const needsLayout = nodes.some(n => (n.x === undefined || n.y === undefined || (n.x === 0 && n.y === 0)))
  return needsLayout ? autoLayout(nodes) : nodes
}
