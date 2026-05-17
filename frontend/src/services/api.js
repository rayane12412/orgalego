// Client REST minimaliste vers le backend FastAPI
// Les chemins sont proxifiés vers http://localhost:8000 par Vite (cf. vite.config.js)

async function request(path, options = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`API ${res.status} sur ${path} : ${text}`)
  }
  if (res.status === 204) return null
  return res.json()
}

// ---------- Blocks ----------

export function fetchBlocks(level = null) {
  const query = level ? `?level=${level}` : ''
  return request(`/blocks${query}`)
}

export function fetchBlock(id) {
  return request(`/blocks/${id}`)
}

// ---------- Projects ----------

export function listProjects() {
  return request('/projects')
}

export function createProject(payload) {
  return request('/projects', { method: 'POST', body: JSON.stringify(payload) })
}

export function updateProject(id, payload) {
  return request(`/projects/${id}`, { method: 'PUT', body: JSON.stringify(payload) })
}

export function deleteProject(id) {
  return request(`/projects/${id}`, { method: 'DELETE' })
}

// ---------- Export ----------

export async function exportPdf(graphUpdate) {
  const res = await fetch('/export/pdf', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(graphUpdate),
  })
  if (!res.ok) throw new Error(`Export PDF a échoué : ${res.status}`)
  return res.blob()
}
