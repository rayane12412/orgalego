import { Handle, Position } from 'reactflow'
import { LEVEL_COLORS, colorForBetweenness } from '../../utils/colors'

// Nœud représentant une Division (niveau macro)
// data : { label, betweenness, isBottleneck, canDrillDown }
export default function DivisionNode({ data }) {
  const colors = LEVEL_COLORS.macro
  const borderColor = data.isBottleneck ? colorForBetweenness(data.betweenness) : colors.border

  return (
    <div
      style={{
        background: colors.bg,
        border: `3px solid ${borderColor}`,
        borderRadius: 12,
        padding: '12px 18px',
        minWidth: 140,
        textAlign: 'center',
        color: colors.text,
        boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
        cursor: data.canDrillDown ? 'pointer' : 'default',
      }}
    >
      <Handle type="target" position={Position.Top} style={{ background: borderColor }} />
      <div style={{ fontWeight: 700, fontSize: 14 }}>{data.label}</div>
      {data.betweenness !== undefined && (
        <div style={{ fontSize: 11, marginTop: 4, opacity: 0.75 }}>
          centralité : {data.betweenness.toFixed(2)}
        </div>
      )}
      {data.canDrillDown && (
        <div style={{ fontSize: 10, marginTop: 4, fontStyle: 'italic' }}>
          cliquer pour explorer ↓
        </div>
      )}
      <Handle type="source" position={Position.Bottom} style={{ background: borderColor }} />
    </div>
  )
}
