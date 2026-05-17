export default function MetricCard({ label, value, hint, color = '#2563eb' }) {
  return (
    <div
      style={{
        background: '#f9fafb',
        border: `1px solid #e5e7eb`,
        borderLeft: `4px solid ${color}`,
        borderRadius: 8,
        padding: '10px 12px',
        marginBottom: 8,
      }}
    >
      <div style={{ fontSize: 11, color: '#6b7280', textTransform: 'uppercase', letterSpacing: 0.4 }}>
        {label}
      </div>
      <div style={{ fontSize: 18, fontWeight: 700, color: '#111827', marginTop: 2 }}>
        {value}
      </div>
      {hint && (
        <div style={{ fontSize: 11, color: '#6b7280', marginTop: 2 }}>{hint}</div>
      )}
    </div>
  )
}
