import { Handle, Position } from 'reactflow'
import { LEVEL_COLORS, colorForBetweenness } from '../../utils/colors'

// Nœud représentant une Équipe (niveau méso)
export default function TeamNode({ data }) {
  const colors = LEVEL_COLORS.meso
  const borderColor = data.isBottleneck ? colorForBetweenness(data.betweenness) : colors.border

  return (
    <div
      style={{
        background: colors.bg,
        border: `2px solid ${borderColor}`,
        borderRadius: 10,
        padding: '10px 14px',
        minWidth: 120,
        textAlign: 'center',
        color: colors.text,
        boxShadow: '0 2px 4px rgba(0,0,0,0.06)',
        cursor: data.canDrillDown ? 'pointer' : 'default',
      }}
    >
      <Handle type="target" position={Position.Top} style={{ background: borderColor }} />
      <div style={{ fontWeight: 600, fontSize: 13 }}>{data.label}</div>
      {data.betweenness !== undefined && (
        <div style={{ fontSize: 10, marginTop: 3, opacity: 0.75 }}>
          centralité : {data.betweenness.toFixed(2)}
        </div>
      )}
      {data.canDrillDown && (
        <div style={{ fontSize: 9, marginTop: 3, fontStyle: 'italic' }}>
          cliquer pour explorer ↓
        </div>
      )}
      <Handle type="source" position={Position.Bottom} style={{ background: borderColor }} />
    </div>
  )
}
