import { useEffect } from 'react';
import { useAnalyticsStore } from '../store/useAnalyticsStore';

export default function Analytics() {
  const { learnerData, isLoading, fetchLearnerData } = useAnalyticsStore();

  useEffect(() => {
    fetchLearnerData();
  }, [fetchLearnerData]);

  if (isLoading) return <div>Loading analytics...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">📊 Your Analytics</h1>
      <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto">
        {JSON.stringify(learnerData, null, 2) || 'No data available yet.'}
      </pre>
    </div>
  );
}
