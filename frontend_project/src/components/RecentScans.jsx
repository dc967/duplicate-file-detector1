
const statusStyles = {
  completed: 'bg-green-50 text-green-600',
  failed: 'bg-red-50 text-red-500',
  partial: 'bg-amber-50 text-amber-600',
}

function RecentScans({ history }) {
  const scans = history || []

  return (
    <div className="bg-white border border-gray-200 rounded-xl">
      <div className="flex items-center justify-between p-5 border-b border-gray-100">
        <div>
          <h3 className="text-sm font-semibold text-gray-800">Recent Scans</h3>
          <p className="text-xs text-gray-400 mt-1">Last scan sessions</p>
        </div>
      </div>

      {scans.length === 0 ? (
        <div className="p-8 text-center">
          <p className="text-xs text-gray-400">No scans yet!</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-5 py-3">Path</th>
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-5 py-3">Files</th>
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-5 py-3">Dups</th>
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-5 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {scans.slice(0, 5).map((scan, index) => (
                <tr key={index} className="border-b border-gray-50 hover:bg-gray-50 transition-all">
                  <td className="px-5 py-3 text-sm font-medium text-gray-700">{scan.path}</td>
                  <td className="px-5 py-3 text-sm text-gray-500">{scan.total_files?.toLocaleString()}</td>
                  <td className="px-5 py-3 text-sm text-gray-500">{scan.duplicates_found?.toLocaleString()}</td>
                  <td className="px-5 py-3">
                    <span className={`text-xs font-medium px-3 py-1 rounded-full ${statusStyles[scan.status] || 'bg-gray-50 text-gray-500'}`}>
                      {scan.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default RecentScans