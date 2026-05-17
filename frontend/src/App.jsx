import { useEffect } from 'react'
import Toolbar from './components/Toolbar/Toolbar'
import Breadcrumb from './components/Breadcrumb/Breadcrumb'
import BlockPalette from './components/BlockPalette/BlockPalette'
import DiagnosisPanel from './components/DiagnosisPanel/DiagnosisPanel'
import GraphView from './components/GraphView/GraphView'
import { useOrgaLegoSocket } from './hooks/useOrgaLegoSocket'
import { useGraphStore } from './store/graphStore'

export default function App() {
  // Établit la connexion WebSocket et synchronise les diagnostics
  useOrgaLegoSocket()

  const setGraph = useGraphStore(s => s.setGraph)

  // Au premier rendu, on tente de charger le cas TechNova en démo
  useEffect(() => {
    fetch('/graph_technova.json')
      .then(r => (r.ok ? r.json() : null))
      .then(data => { if (data) setGraph(data) })
      .catch(() => { /* silent : l'utilisateur peut charger manuellement */ })
  }, [setGraph])

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Toolbar />
      <Breadcrumb />
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        <BlockPalette />
        <main style={{ flex: 1, background: '#f6f7f9' }}>
          <GraphView />
        </main>
        <DiagnosisPanel />
      </div>
    </div>
  )
}
