import { Handle, Position } from 'reactflow'
import { LEVEL_COLORS, colorForBetweenness, colorForWorkload } from '../../utils/colors'

// Nœud représentant un individu (niveau micro)
export default function PersonNode({ data }) {
  const colors = LEVEL_COLORS.micro
  const borderColor = data.isBottleneck
    ? colorForBetweenness(data.betweenness)
    : data.workload >= 0.85
    ? colorForWorkload(data.workload)
    : colors.border

  return (
    <div
      style={{
        background: colors.bg,
        border: `2px solid ${borderColor}`,
        borderRadius: '50%',
        width: 90,
        height: 90,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        color: colors.text,
        boxShadow: '0 2px 4px rgba(0,0,0,0.06)',
        textAlign: 'center',
        padding: 4,
      }}
    >
      <Handle type="target" position={Position.Top} style={{ background: borderColor }} />
      <div style={{ fontWeight: 600, fontSize: 11, lineHeight: 1.2 }}>{data.label}</div>
      {data.betweenness !== undefined && (
        <div style={{ fontSize: 9, marginTop: 2, opacity: 0.7 }}>
          {data.betweenness.toFixed(2)}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} style={{ background: borderColor }} />
    </div>
  )
}
