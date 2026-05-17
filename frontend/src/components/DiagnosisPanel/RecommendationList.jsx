import { SEVERITY_COLORS } from '../../utils/colors'

const SEVERITY_ICON = { info: 'ℹ', warning: '⚠', critical: '⛔' }

export default function RecommendationList({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div style={{ fontSize: 12, color: '#6b7280', padding: 8 }}>
        Aucune recommandation pour l'instant.
      </div>
    )
  }

  return (
    <div>
      {recommendations.map((reco, i) => {
        const c = SEVERITY_COLORS[reco.severity] || SEVERITY_COLORS.info
        return (
          <div
            key={i}
            style={{
              background: c.bg,
              border: `1px solid ${c.border}`,
              borderRadius: 8,
              padding: '8px 10px',
              marginBottom: 8,
              color: c.text,
              fontSize: 12,
              lineHeight: 1.4,
            }}
          >
            <div style={{ fontWeight: 700, marginBottom: 2 }}>
              {SEVERITY_ICON[reco.severity]} {reco.severity.toUpperCase()}
            </div>
            <div>{reco.message}</div>
            {reco.related_nodes?.length > 0 && (
              <div style={{ fontSize: 10, marginTop: 4, fontStyle: 'italic' }}>
                Concerne : {reco.related_nodes.join(', ')}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
