import { useEffect } from 'react'
import StatsCards from '../components/StatsCards'
import ScanSummary from '../components/ScanSummary'
import RecentScans from '../components/RecentScans'
import { useScan } from '../context/ScanContext'

function Dashboard() {
  const { stats, history, fetchStats, fetchHistory } = useScan()

  useEffect(() => {
    fetchStats()
    fetchHistory()
  }, [])

  return (
    <div>
      <StatsCards stats={stats} />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ScanSummary />
        <RecentScans history={history} />
      </div>
    </div>
  )
}

export default Dashboard