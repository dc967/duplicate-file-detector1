import { useState, useEffect } from 'react'
import DuplicateTable from '../components/DuplicateTable'
import { useScan } from '../context/ScanContext'

const tabs = [
  { label: 'All', value: 'all' },
  { label: 'Images', value: 'image' },
  { label: 'Documents', value: 'document' },
  { label: 'Videos', value: 'video' },
  { label: 'Archives', value: 'archive' },
]

function ScanResults() {
  const [activeTab, setActiveTab] = useState('all')
  const { scanResults } = useScan()

  const allData = scanResults?.duplicates?.map((group, index) => ({
    id: index + 1,
    name: group.copies[0]?.name || 'Unknown',
    ext: group.copies[0]?.extension || 'FILE',
    size: group.size_formatted || '0 KB',
    copies: group.copies_count,
    hash: group.hash,
    path: group.copies[0]?.path || '',
    type: group.file_type,
  })) || []

  const filteredData = activeTab === 'all'
    ? allData
    : allData.filter((item) => item.type === activeTab)

  return (
    <div>
      {/* Tabs */}
      <div className="flex gap-2 mb-4 flex-wrap">
        {tabs.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setActiveTab(tab.value)}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all
              ${activeTab === tab.value
                ? 'bg-white text-gray-800 shadow-sm border border-gray-200'
                : 'text-gray-500 hover:bg-white hover:text-gray-700'
              }`}
          >
            {tab.label} ({allData.filter(i => tab.value === 'all' ? true : i.type === tab.value).length})
          </button>
        ))}
      </div>

      {/* No Results */}
      {allData.length === 0 && (
        <div className="bg-white border border-gray-200 rounded-xl p-10 text-center">
          <p className="text-gray-400 text-sm">No scan results yet!</p>
          <p className="text-gray-300 text-xs mt-1">Go to Upload page and start a scan</p>
        </div>
      )}

      {/* Duplicate Table */}
      {allData.length > 0 && (
        <DuplicateTable data={filteredData} />
      )}
    </div>
  )
}

export default ScanResults