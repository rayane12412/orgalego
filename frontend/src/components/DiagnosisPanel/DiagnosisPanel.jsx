import { useGraphStore } from '../../store/graphStore'
import MetricCard from './MetricCard'
import RecommendationList from './RecommendationList'

export default function DiagnosisPanel() {
  const diagnosis = useGraphStore(s => s.diagnosis)
  const isLoading = useGraphStore(s => s.isLoading)
  const error = useGraphStore(s => s.error)

  return (
    <aside
      style={{
        width: 320,
        background: '#ffffff',
        borderLeft: '1px solid #e5e7eb',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
      }}
    >
      <div style={{ padding: '12px 16px', borderBottom: '1px solid #e5e7eb' }}>
        <h2 style={{ margin: 0, fontSize: 16 }}>Diagnostic</h2>
        {isLoading && (
          <span style={{ fontSize: 11, color: '#6b7280' }}>calcul en cours…</span>
        )}
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
        {error && (
          <div style={{ fontSize: 12, color: '#dc2626', marginBottom: 8 }}>
            {typeof error === 'string' ? error : 'Erreur de communication avec le backend'}
          </div>
        )}

        {!diagnosis && !isLoading && (
          <div style={{ fontSize: 12, color: '#6b7280' }}>
            Ajoutez des blocs pour démarrer le diagnostic.
          </div>
        )}

        {diagnosis && (
          <>
            {diagnosis.community_result && (
              <MetricCard
                label="Modularité (Louvain)"
                value={diagnosis.community_result.modularity}
                hint={
                  diagnosis.community_result.is_siloed
                    ? `${diagnosis.community_result.n_communities} silos détectés`
                    : `${diagnosis.community_result.n_communities} communautés, pas de silo`
                }
                color={diagnosis.community_result.is_siloed ? '#dc2626' : '#16a34a'}
              />
            )}

            {diagnosis.best_archetype && (
              <MetricCard
                label="Archétype dominant"
                value={diagnosis.best_archetype.archetype_name}
                hint={`École ${diagnosis.best_archetype.school} · similarité ${diagnosis.best_archetype.similarity}`}
                color="#0d9488"
              />
            )}

            {diagnosis.node_metrics?.length > 0 && (
              <MetricCard
                label="Goulots détectés"
                value={diagnosis.node_metrics.filter(m => m.is_bottleneck).length}
                hint={
                  diagnosis.node_metrics[0]
                    ? `Plus central : ${diagnosis.node_metrics[0].node_id} (${diagnosis.node_metrics[0].betweenness})`
                    : ''
                }
                color={
                  diagnosis.node_metrics.some(m => m.is_bottleneck) ? '#ea580c' : '#16a34a'
                }
              />
            )}

            <h3 style={{ fontSize: 13, marginTop: 16, marginBottom: 8, color: '#374151' }}>
              Recommandations
            </h3>
            <RecommendationList recommendations={diagnosis.recommendations} />
          </>
        )}
      </div>
    </aside>
  )
}
