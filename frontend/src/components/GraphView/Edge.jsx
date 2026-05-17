// Helpers pour styliser les arêtes selon leur type
// React Flow gère le rendu par défaut, on lui passe juste un style

import { EDGE_COLORS } from '../../utils/colors'

export function styleForEdgeType(type, frequency = 1) {
  const stroke = EDGE_COLORS[type] || '#94a3b8'
  const baseWidth = Math.min(1 + frequency * 0.5, 4)
  return {
    stroke,
    strokeWidth: baseWidth,
    strokeDasharray: type === 'informal' ? '6,3' : undefined,
  }
}

// Composant React purement décoratif si on veut un edge custom (non utilisé pour le MVP)
export default function CustomEdge() {
  return null
}
