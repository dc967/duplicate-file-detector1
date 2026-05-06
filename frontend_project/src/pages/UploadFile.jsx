import FileUploader from '../components/FileUploader'
import ScanProgress from '../components/ScanProgress'
import { useState } from 'react'
import { useScan } from '../context/ScanContext'
import { useNavigate } from 'react-router-dom'

function UploadFile() {
  const [path, setPath] = useState('')
  const [recursive, setRecursive] = useState(true)
  const [skipSystem, setSkipSystem] = useState(true)
  const [hashMethod, setHashMethod] = useState('sha256')
  const [error, setError] = useState('')

  const { startScan, isScanning, progress } = useScan()
  const navigate = useNavigate()

  const handleFileSelect = (files) => {
    console.log('Files selected:', files)
  }

  const handleScan = async () => {
    if (!path.trim()) {
      setError('Please enter a directory path!')
      return
    }
    setError('')
    try {
      await startScan(path, {
        recursive,
        skip_system: skipSystem,
        hash_method: hashMethod,
      })
      navigate('/results')
    } catch (err) {
      setError(err.response?.data?.detail || 'Scan failed!')
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

      {/* Left Side */}
      <div className="bg-white border border-gray-200 rounded-xl">
        <div className="p-5 border-b border-gray-100">
          <h3 className="text-sm font-semibold text-gray-800">Upload Files or Folder</h3>
        </div>
        <div className="p-5">
          <FileUploader onFileSelect={handleFileSelect} />

          {/* Directory Path */}
          <div className="mt-4">
            <label className="text-xs font-medium text-gray-600 mb-1 block">
              Or enter directory path
            </label>
            <input
              type="text"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              placeholder="/home/user/Documents"
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
            />
          </div>

          {/* Error */}
          {error && (
            <p className="text-xs text-red-500 mt-2">{error}</p>
          )}

          {/* Scan Button */}
          <button
            onClick={handleScan}
            disabled={isScanning}
            className="mt-4 w-full bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white text-sm font-semibold py-2.5 rounded-lg transition-all"
          >
            {isScanning ? 'Scanning...' : 'Start Scan'}
          </button>
        </div>
      </div>

      {/* Right Side */}
      <div className="bg-white border border-gray-200 rounded-xl">
        <div className="p-5 border-b border-gray-100">
          <h3 className="text-sm font-semibold text-gray-800">Scan Options</h3>
        </div>
        <div className="p-5">

          {/* Hash Method */}
          <div className="mb-4">
            <label className="text-xs font-medium text-gray-600 mb-1 block">Hash Method</label>
            <select
              value={hashMethod}
              onChange={(e) => setHashMethod(e.target.value)}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
            >
              <option value="md5">MD5 (Fast)</option>
              <option value="sha256">SHA-256 (Recommended)</option>
              <option value="sha512">SHA-512 (Secure)</option>
            </select>
          </div>

          {/* Recursive Toggle */}
          <div className="flex items-center justify-between py-3 border-b border-gray-50">
            <div>
              <p className="text-sm font-medium text-gray-700">Recursive Scan</p>
              <p className="text-xs text-gray-400 mt-0.5">Scan all subdirectories</p>
            </div>
            <button
              onClick={() => setRecursive(!recursive)}
              className={`w-10 h-5 rounded-full transition-all relative ${recursive ? 'bg-blue-500' : 'bg-gray-200'}`}
            >
              <span className={`absolute top-0.5 w-4 h-4 bg-white rounded-full transition-all ${recursive ? 'left-5' : 'left-0.5'}`}></span>
            </button>
          </div>

          {/* Skip System Files Toggle */}
          <div className="flex items-center justify-between py-3">
            <div>
              <p className="text-sm font-medium text-gray-700">Skip System Files</p>
              <p className="text-xs text-gray-400 mt-0.5">Exclude OS critical files</p>
            </div>
            <button
              onClick={() => setSkipSystem(!skipSystem)}
              className={`w-10 h-5 rounded-full transition-all relative ${skipSystem ? 'bg-blue-500' : 'bg-gray-200'}`}
            >
              <span className={`absolute top-0.5 w-4 h-4 bg-white rounded-full transition-all ${skipSystem ? 'left-5' : 'left-0.5'}`}></span>
            </button>
          </div>

        </div>
      </div>

      {/* Scan Progress */}
      {isScanning && (
        <div className="col-span-2">
          <ScanProgress
            progress={progress}
            scanned={0}
            total={0}
            currentFile=""
            isScanning={isScanning}
          />
        </div>
      )}

    </div>
  )
}

export default UploadFile