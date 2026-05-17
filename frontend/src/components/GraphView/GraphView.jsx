import { useMemo, useCallback } from 'react'
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow'
import 'reactflow/dist/style.css'

import DivisionNode from './DivisionNode'
import TeamNode from './TeamNode'
import PersonNode from './PersonNode'
import { styleForEdgeType } from './Edge'

import { useGraphStore } from '../../store/graphStore'
import { useNavigationStore } from '../../store/navigationStore'
import { ensurePositions } from '../../utils/layout2d'

const nodeTypes = {
  division: DivisionNode,
  team: TeamNode,
  person: PersonNode,
}

// Mappe niveau -> type de nœud React Flow
const NODE_TYPE_BY_LEVEL = {
  macro: 'division',
  meso: 'team',
  micro: 'person',
}

export default function GraphView() {
  const graph = useGraphStore(s => s.graph)
  const diagnosis = useGraphStore(s => s.diagnosis)
  const updateNodePosition = useGraphStore(s => s.updateNodePosition)

  const current = useNavigationStore(s => s.current())
  const drillDown = useNavigationStore(s => s.drillDown)

  // Sélection des nœuds/arêtes du niveau courant + filtrage par parent
  const { rfNodes, rfEdges } = useMemo(() => {
    const level = current.level
    const allNodes = graph[`${level}_nodes`] || []
    const allEdges = graph[`${level}_edges`] || []

    // Filtrer selon le parent si on n'est pas à la racine macro
    let filteredNodes = allNodes
    if (level === 'meso' && current.parent) {
      const childIds = new Set(
        graph.memberships_macro_meso
          .filter(m => m.parent === current.parent)
          .map(m => m.child),
      )
      filteredNodes = allNodes.filter(n => childIds.has(n.id))
    } else if (level === 'micro' && current.parent) {
      const childIds = new Set(
        graph.memberships_meso_micro
          .filter(m => m.parent === current.parent)
          .map(m => m.child),
      )
      filteredNodes = allNodes.filter(n => childIds.has(n.id))
    }

    const visibleIds = new Set(filteredNodes.map(n => n.id))
    const positioned = ensurePositions(filteredNodes)

    // Lookup des métriques de diagnostic
    const metricsById = {}
    if (diagnosis?.node_metrics) {
      diagnosis.node_metrics.forEach(m => {
        metricsById[m.node_id] = m
      })
    }

    // L'utilisateur peut descendre tant qu'il n'est pas au niveau micro
    const canDrillDown = level !== 'micro'

    const rfNodes = positioned.map(n => {
      const m = metricsById[n.id]
      return {
        id: n.id,
        type: NODE_TYPE_BY_LEVEL[level],
        position: { x: n.x ?? 0, y: n.y ?? 0 },
        data: {
          label: n.label,
          betweenness: m?.betweenness,
          isBottleneck: m?.is_bottleneck,
          workload: n.workload,
          canDrillDown,
        },
      }
    })

    const rfEdges = allEdges
      .filter(e => visibleIds.has(e.source) && visibleIds.has(e.target))
      .map(e => ({
        id: e.id,
        source: e.source,
        target: e.target,
        type: 'default',
        style: styleForEdgeType(e.type, e.frequency),
        animated: e.type === 'informal',
      }))

    return { rfNodes, rfEdges }
  }, [graph, current, diagnosis])

  // Clic sur un nœud → descente d'un niveau
  const onNodeClick = useCallback(
    (event, node) => {
      if (current.level === 'micro') return // déjà au plus bas
      const nextLevel = current.level === 'macro' ? 'meso' : 'micro'
      drillDown(nextLevel, node.id, node.data.label)
    },
    [current.level, drillDown],
  )

  // Drag d'un nœud → mise à jour de sa position dans le store
  const onNodeDragStop = useCallback(
    (event, node) => {
      updateNodePosition(current.level, node.id, node.position.x, node.position.y)
    },
    [current.level, updateNodePosition],
  )

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ReactFlow
        nodes={rfNodes}
        edges={rfEdges}
        nodeTypes={nodeTypes}
        onNodeClick={onNodeClick}
        onNodeDragStop={onNodeDragStop}
        fitView
        fitViewOptions={{ padding: 0.2 }}
      >
        <Background gap={20} color="#e5e7eb" />
        <Controls />
        <MiniMap pannable zoomable style={{ background: '#f3f4f6' }} />
      </ReactFlow>
    </div>
  )
}
