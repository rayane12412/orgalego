import { useEffect, useState } from 'react'
import { fetchBlocks } from '../services/api'

// Charge la bibliothèque de blocs depuis le backend au montage
export function useBlockLibrary(level = null) {
  const [blocks, setBlocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    fetchBlocks(level)
      .then(data => {
        if (!cancelled) {
          setBlocks(data)
          setError(null)
        }
      })
      .catch(err => {
        if (!cancelled) setError(err.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => { cancelled = true }
  }, [level])

  return { blocks, loading, error }
}
