/**
 * Course catalog page — displays iGOT and local courses.
 */
import { useState } from 'react';

export default function Courses() {
  const [search, setSearch] = useState('');
  const [domain, setDomain] = useState('all');

  const domains = ['all', 'statistical', 'technical', 'digital_governance', 'behavioural'];

  // Mock data — will be replaced with API call
  const courses = [
    { id: '1', title: 'Principles of Survey Design', domain: 'statistical', duration: '8 hours', difficulty: 'Beginner' },
    { id: '2', title: 'Sampling Techniques for Official Statistics', domain: 'statistical', duration: '12 hours', difficulty: 'Intermediate' },
    { id: '3', title: 'National Accounts Methodology', domain: 'statistical', duration: '16 hours', difficulty: 'Advanced' },
    { id: '4', title: 'Digital Governance Framework', domain: 'digital_governance', duration: '6 hours', difficulty: 'Beginner' },
  ];

  const filtered = courses.filter(c => {
    const matchSearch = c.title.toLowerCase().includes(search.toLowerCase());
    const matchDomain = domain === 'all' || c.domain === domain;
    return matchSearch && matchDomain;
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">📚 Course Catalog</h1>

      {/* Filters */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search courses..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="flex-1 border rounded-lg px-4 py-2"
        />
        <select value={domain} onChange={e => setDomain(e.target.value)} className="border rounded-lg px-4 py-2">
          {domains.map(d => <option key={d} value={d}>{d === 'all' ? 'All Domains' : d.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}</option>)}
        </select>
      </div>

      {/* Course Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(course => (
          <div key={course.id} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full">
                {course.domain.replace('_', ' ')}
              </span>
              <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                course.difficulty === 'Beginner' ? 'bg-green-100 text-green-700' :
                course.difficulty === 'Intermediate' ? 'bg-yellow-100 text-yellow-700' :
                'bg-red-100 text-red-700'
              }`}>{course.difficulty}</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">{course.title}</h3>
            <p className="text-sm text-gray-500 mb-4">{course.duration}</p>
            <button className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700">
              Enroll Now
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
