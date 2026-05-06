import { createContext, useContext, useState } from 'react'
import { scanAPI } from '../services/api'

const ScanContext = createContext()

export function ScanProvider({ children }) {
  const [scanResults, setScanResults] = useState(null)
  const [stats, setStats] = useState(null)
  const [history, setHistory] = useState([])
  const [isScanning, setIsScanning] = useState(false)
  const [progress, setProgress] = useState(0)

  const startScan = async (path, options) => {
    setIsScanning(true)
    setProgress(0)
    try {
      const response = await scanAPI.startScan(path, options)
      setScanResults(response.data)
      await fetchStats()
      await fetchHistory()
      return response.data
    } finally {
      setIsScanning(false)
      setProgress(100)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await scanAPI.getStats()
      setStats(response.data)
    } catch (error) {
      console.error('Stats fetch failed:', error)
    }
  }

  const fetchHistory = async () => {
    try {
      const response = await scanAPI.getHistory()
      setHistory(response.data.history || [])
    } catch (error) {
      console.error('History fetch failed:', error)
    }
  }

  return (
    <ScanContext.Provider value={{
      scanResults,
      stats,
      history,
      isScanning,
      progress,
      startScan,
      fetchStats,
      fetchHistory,
    }}>
      {children}
    </ScanContext.Provider>
  )
}

export function useScan() {
  return useContext(ScanContext)
}