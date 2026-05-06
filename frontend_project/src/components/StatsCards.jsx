import { File, Copy, HardDrive, Clock } from 'lucide-react'

function StatCard({ icon, value, label, subText, subColor, iconBg }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 flex items-center gap-4">
      <div className={`w-11 h-11 rounded-lg flex items-center justify-center flex-shrink-0 ${iconBg}`}>
        {icon}
      </div>
      <div>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
        <p className="text-xs text-gray-500 font-medium mt-0.5">{label}</p>
        <p className={`text-xs font-medium mt-1 ${subColor}`}>{subText}</p>
      </div>
    </div>
  )
}

function StatsCards({ stats }) {
  const cards = [
    {
      icon: <File size={20} />,
      value: stats?.total_files?.toLocaleString() || '0',
      label: 'Total Files Scanned',
      subText: `${stats?.total_scans || 0} total scans`,
      subColor: 'text-green-500',
      iconBg: 'bg-blue-50 text-blue-500',
    },
    {
      icon: <Copy size={20} />,
      value: stats?.total_duplicates?.toLocaleString() || '0',
      label: 'Duplicates Found',
      subText: 'From last scan',
      subColor: 'text-red-500',
      iconBg: 'bg-red-50 text-red-500',
    },
    {
      icon: <HardDrive size={20} />,
      value: stats?.space_recoverable || '0 KB',
      label: 'Space Recoverable',
      subText: 'Can be freed',
      subColor: 'text-green-500',
      iconBg: 'bg-green-50 text-green-500',
    },
    {
      icon: <Clock size={20} />,
      value: stats?.total_scans || '0',
      label: 'Total Scans',
      subText: 'All time',
      subColor: 'text-gray-400',
      iconBg: 'bg-amber-50 text-amber-500',
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {cards.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  )
}

export default StatsCards