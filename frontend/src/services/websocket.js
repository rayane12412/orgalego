// Wrapper WebSocket avec reconnexion automatique simple

const WS_URL = `ws://${window.location.hostname}:8000/ws/graph`

export class OrgaLegoSocket {
  constructor() {
    this.ws = null
    this.listeners = new Set()
    this.shouldReconnect = true
    this.reconnectDelay = 1500
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return
    }

    this.ws = new WebSocket(WS_URL)

    this.ws.onopen = () => {
      // Optionnel : envoyer un ping initial
    }

    this.ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data)
        this.listeners.forEach(fn => fn(msg))
      } catch (err) {
        console.warn('Message WebSocket invalide :', event.data)
      }
    }

    this.ws.onclose = () => {
      if (this.shouldReconnect) {
        setTimeout(() => this.connect(), this.reconnectDelay)
      }
    }

    this.ws.onerror = (err) => {
      console.warn('Erreur WebSocket :', err)
    }
  }

  send(payload) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(payload))
    }
  }

  sendGraphUpdate(graph, focusLevel = 'macro', focusNodeId = null) {
    this.send({
      type: 'graph_update',
      payload: { graph, focus_level: focusLevel, focus_node_id: focusNodeId },
    })
  }

  onMessage(callback) {
    this.listeners.add(callback)
    return () => this.listeners.delete(callback)
  }

  disconnect() {
    this.shouldReconnect = false
    if (this.ws) this.ws.close()
  }
}

// Singleton partagé
export const orgaLegoSocket = new OrgaLegoSocket()
