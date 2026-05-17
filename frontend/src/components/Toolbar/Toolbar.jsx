import { useGraphStore } from '../../store/graphStore'
import { useNavigationStore } from '../../store/navigationStore'
import { exportPdf } from '../../services/api'

export default function Toolbar() {
  const graph = useGraphStore(s => s.graph)
  const current = useNavigationStore(s => s.current())
  const reset = useNavigationStore(s => s.reset)
  const setGraph = useGraphStore(s => s.setGraph)

  async function handleExport() {
    try {
      const blob = await exportPdf({
        graph,
        focus_level: current.level,
        focus_node_id: current.parent,
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'orgalego_diagnosis.pdf'
      link.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      alert('Export PDF impossible : ' + e.message)
    }
  }

  async function handleLoadTechnova() {
    try {
      const res = await fetch('/graph_technova.json')
      const data = await res.json()
      setGraph(data)
      reset()
    } catch (e) {
      alert(
        'Impossible de charger le cas TechNova. Vérifie que graph_technova.json est bien dans frontend/public/.',
      )
    }
  }

  function handleClear() {
    setGraph({
      macro_nodes: [], macro_edges: [],
      meso_nodes: [], meso_edges: [],
      micro_nodes: [], micro_edges: [],
      memberships_macro_meso: [], memberships_meso_micro: [],
    })
    reset()
  }

  const btnStyle = {
    padding: '6px 14px',
    fontSize: 13,
    background: '#ffffff',
    border: '1px solid #d1d5db',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: 500,
    color: '#374151',
  }

  return (
    <header
      style={{
        height: 56,
        background: '#1e3a8a',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        padding: '0 20px',
        gap: 16,
        borderBottom: '1px solid #1e40af',
      }}
    >
      <h1 style={{ margin: 0, fontSize: 18, fontWeight: 700 }}>OrgaLego</h1>
      <span style={{ fontSize: 12, opacity: 0.8 }}>
        Simulateur de structures organisationnelles · v0.1
      </span>

      <div style={{ flex: 1 }} />

      <button onClick={handleLoadTechnova} style={btnStyle}>
        Charger TechNova
      </button>
      <button onClick={handleClear} style={btnStyle}>
        Vider
      </button>
      <button onClick={handleExport} style={{ ...btnStyle, background: '#16a34a', color: 'white', borderColor: '#15803d' }}>
        Exporter PDF
      </button>
    </header>
  )
}
