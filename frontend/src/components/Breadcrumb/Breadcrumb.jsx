import { useNavigationStore } from '../../store/navigationStore'

const LEVEL_LABEL = {
  macro: 'Macro',
  meso: 'Méso',
  micro: 'Micro',
}

export default function Breadcrumb() {
  const path = useNavigationStore(s => s.path)
  const goTo = useNavigationStore(s => s.goTo)

  return (
    <nav
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        padding: '8px 16px',
        background: '#ffffff',
        borderBottom: '1px solid #e5e7eb',
        fontSize: 14,
      }}
    >
      <span style={{ fontWeight: 600, color: '#6b7280', marginRight: 4 }}>Navigation :</span>
      {path.map((step, index) => {
        const isLast = index === path.length - 1
        return (
          <span key={`${step.level}-${index}`} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <button
              onClick={() => goTo(index)}
              disabled={isLast}
              style={{
                background: 'none',
                border: 'none',
                cursor: isLast ? 'default' : 'pointer',
                color: isLast ? '#111827' : '#2563eb',
                fontWeight: isLast ? 600 : 500,
                padding: '4px 8px',
                borderRadius: 6,
                textDecoration: isLast ? 'none' : 'underline',
              }}
            >
              {step.parentLabel} <span style={{ opacity: 0.6, fontSize: 12 }}>({LEVEL_LABEL[step.level]})</span>
            </button>
            {!isLast && <span style={{ color: '#9ca3af' }}>›</span>}
          </span>
        )
      })}
    </nav>
  )
}
