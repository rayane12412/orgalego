import { useState } from 'react'
import { useBlockLibrary } from '../../hooks/useBlockLibrary'
import { useGraphStore } from '../../store/graphStore'
import BlockCard from './BlockCard'

const TABS = [
  { level: 'macro', label: 'Macro' },
  { level: 'meso',  label: 'Méso' },
  { level: 'micro', label: 'Micro' },
]

export default function BlockPalette() {
  const [activeTab, setActiveTab] = useState('macro')
  const { blocks, loading, error } = useBlockLibrary()
  const insertBlock = useGraphStore(s => s.insertBlock)

  const filtered = blocks.filter(b => b.level === activeTab)

  return (
    <aside
      style={{
        width: 280,
        background: '#ffffff',
        borderRight: '1px solid #e5e7eb',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
      }}
    >
      <div style={{ padding: '12px 16px', borderBottom: '1px solid #e5e7eb' }}>
        <h2 style={{ margin: 0, fontSize: 16 }}>Bibliothèque Lego</h2>
        <p style={{ margin: '4px 0 0', fontSize: 11, color: '#6b7280' }}>
          Cliquez pour insérer un archétype théorique dans le graphe.
        </p>
      </div>

      <div style={{ display: 'flex', borderBottom: '1px solid #e5e7eb' }}>
        {TABS.map(t => (
          <button
            key={t.level}
            onClick={() => setActiveTab(t.level)}
            style={{
              flex: 1,
              padding: '8px 4px',
              background: activeTab === t.level ? '#f3f4f6' : 'transparent',
              border: 'none',
              borderBottom: activeTab === t.level ? '2px solid #2563eb' : '2px solid transparent',
              cursor: 'pointer',
              fontSize: 12,
              fontWeight: 600,
              color: activeTab === t.level ? '#111827' : '#6b7280',
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
        {loading && <div style={{ fontSize: 12 }}>Chargement…</div>}
        {error && <div style={{ fontSize: 12, color: '#dc2626' }}>Erreur : {error}</div>}
        {!loading && !error && filtered.length === 0 && (
          <div style={{ fontSize: 12, color: '#6b7280' }}>Aucun bloc à ce niveau.</div>
        )}
        {filtered.map(b => (
          <BlockCard key={b.id} block={b} onInsert={insertBlock} />
        ))}
      </div>
    </aside>
  )
}
