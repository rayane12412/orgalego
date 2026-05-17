import { LEVEL_COLORS } from '../../utils/colors'

export default function BlockCard({ block, onInsert }) {
  const colors = LEVEL_COLORS[block.level] || LEVEL_COLORS.macro

  return (
    <div
      style={{
        background: colors.bg,
        border: `1px solid ${colors.border}`,
        borderRadius: 8,
        padding: 10,
        marginBottom: 8,
        color: colors.text,
      }}
    >
      <div style={{ fontWeight: 600, fontSize: 13 }}>{block.name}</div>
      <div style={{ fontSize: 11, opacity: 0.75, marginTop: 2 }}>
        {block.school} · {block.level}
      </div>
      {block.description && (
        <div style={{ fontSize: 11, marginTop: 6, lineHeight: 1.35 }}>
          {block.description}
        </div>
      )}
      <button
        onClick={() => onInsert(block)}
        style={{
          marginTop: 8,
          width: '100%',
          padding: '6px 10px',
          fontSize: 12,
          background: colors.border,
          color: 'white',
          border: 'none',
          borderRadius: 6,
          cursor: 'pointer',
          fontWeight: 600,
        }}
      >
        + Ajouter au graphe
      </button>
    </div>
  )
}
