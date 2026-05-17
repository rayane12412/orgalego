// Couleurs des nœuds selon métriques de diagnostic

export const LEVEL_COLORS = {
  macro: { bg: '#dbeafe', border: '#2563eb', text: '#1e3a8a' },
  meso:  { bg: '#ccfbf1', border: '#0d9488', text: '#134e4a' },
  micro: { bg: '#fed7aa', border: '#ea580c', text: '#7c2d12' },
}

export const EDGE_COLORS = {
  hierarchy:     '#2563eb',
  functional:    '#0d9488',
  collaboration: '#a16207',
  informal:      '#dc2626',
}

// Couleur selon centralité d'intermédiarité (vert -> orange -> rouge)
export function colorForBetweenness(score) {
  if (score >= 0.5) return '#dc2626' // rouge : goulot critique
  if (score >= 0.3) return '#ea580c' // orange : surveillance
  if (score >= 0.1) return '#ca8a04' // jaune : intermédiaire
  return '#16a34a'                   // vert : sain
}

// Couleur selon charge de travail
export function colorForWorkload(workload) {
  if (workload >= 0.85) return '#dc2626'
  if (workload >= 0.7)  return '#ea580c'
  return '#16a34a'
}

// Sévérité des recommandations
export const SEVERITY_COLORS = {
  info:     { bg: '#dbeafe', border: '#2563eb', text: '#1e3a8a' },
  warning:  { bg: '#fef3c7', border: '#ca8a04', text: '#78350f' },
  critical: { bg: '#fee2e2', border: '#dc2626', text: '#7f1d1d' },
}
