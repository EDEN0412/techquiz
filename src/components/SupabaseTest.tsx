import { useState } from 'react'
import { supabase, testSupabaseConnection } from '../lib/supabaseClient'

const SupabaseTest = () => {
  const [testResult, setTestResult] = useState<{
    success?: boolean;
    data?: any;
    error?: any;
  }>({})
  const [loading, setLoading] = useState(false)

  const handleTestConnection = async () => {
    setLoading(true)
    try {
      const result = await testSupabaseConnection()
      setTestResult(result)
    } catch (error) {
      setTestResult({ success: false, error })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden">
      <h2 className="text-xl font-bold mb-4">Supabase接続テスト</h2>
      
      <button
        onClick={handleTestConnection}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? '接続中...' : '接続テスト実行'}
      </button>

      {testResult.success !== undefined && (
        <div className="mt-4 p-3 border rounded">
          <p className={`font-bold ${testResult.success ? 'text-green-600' : 'text-red-600'}`}>
            {testResult.success ? '接続成功！' : '接続失敗'}
          </p>
          
          {testResult.data && (
            <pre className="mt-2 text-sm bg-gray-100 p-2 rounded overflow-auto">
              {JSON.stringify(testResult.data, null, 2)}
            </pre>
          )}
          
          {testResult.error && (
            <pre className="mt-2 text-sm bg-red-50 text-red-800 p-2 rounded overflow-auto">
              {JSON.stringify(testResult.error, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  )
}

export default SupabaseTest 