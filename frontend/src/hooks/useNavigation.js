// Re-export du store de navigation
export { useNavigationStore } from '../store/navigationStore'

import { useNavigationStore } from '../store/navigationStore'

// Helper qui renvoie un sous-ensemble du store : couramment utilisé
export function useCurrentLevel() {
  return useNavigationStore(s => s.current())
}
