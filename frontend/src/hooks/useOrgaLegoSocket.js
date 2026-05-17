import { useEffect, useRef } from 'react'
import { orgaLegoSocket } from '../services/websocket'
import { useGraphStore } from '../store/graphStore'
import { useNavigationStore } from '../store/navigationStore'

// Hook qui établit la connexion WebSocket et synchronise les mises à jour
// du graphe avec le backend pour recevoir les diagnostics en temps réel.
export function useOrgaLegoSocket() {
  const { graph, setDiagnosis, setLoading, setError } = useGraphStore()
  const current = useNavigationStore(s => s.current())
  const debounceTimer = useRef(null)

  // Connexion + abonnement aux messages entrants
  useEffect(() => {
    orgaLegoSocket.connect()
    const unsubscribe = orgaLegoSocket.onMessage((msg) => {
      if (msg.type === 'diagnosis_result') {
        setDiagnosis(msg.payload)
        setLoading(false)
        setError(null)
      } else if (msg.type === 'error') {
        setError(msg.payload)
        setLoading(false)
      }
    })
    return () => {
      unsubscribe()
    }
  }, [setDiagnosis, setLoading, setError])

  // Envoie une mise à jour à chaque changement du graphe ou du focus (debounced)
  useEffect(() => {
    if (debounceTimer.current) clearTimeout(debounceTimer.current)
    debounceTimer.current = setTimeout(() => {
      setLoading(true)
      orgaLegoSocket.sendGraphUpdate(graph, current.level, current.parent)
    }, 200)
    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current)
    }
  }, [graph, current.level, current.parent, setLoading])
}
