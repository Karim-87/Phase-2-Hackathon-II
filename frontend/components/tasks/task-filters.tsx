import { useState, useEffect } from 'react';
import { PriorityLevel } from '@/types/task';

interface TaskFiltersProps {
  onFilterChange: (filters: {
    priority?: PriorityLevel;
    completed?: boolean;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => void;
}

export default function TaskFilters({ onFilterChange }: TaskFiltersProps) {
  const [priority, setPriority] = useState<PriorityLevel | ''>('');
  const [completed, setCompleted] = useState<boolean | null>(null);
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    // Apply filters when any filter value changes
    onFilterChange({
      priority: priority || undefined,
      completed: completed === null ? undefined : completed,
      sortBy,
      sortOrder,
    });
  }, [priority, completed, sortBy, sortOrder]);

  const handleReset = () => {
    setPriority('');
    setCompleted(null);
    setSortBy('created_at');
    setSortOrder('desc');
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value as PriorityLevel || '')}
            className="w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
          >
            <option value="">All Priorities</option>
            <option value="urgent_important">Urgent & Important</option>
            <option value="urgent_not_important">Urgent & Not Important</option>
            <option value="not_urgent_important">Not Urgent & Important</option>
            <option value="not_urgent_not_important">Not Urgent & Not Important</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            value={completed === null ? '' : completed.toString()}
            onChange={(e) => setCompleted(e.target.value === '' ? null : e.target.value === 'true')}
            className="w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
          >
            <option value="">All Tasks</option>
            <option value="false">Pending</option>
            <option value="true">Completed</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
          >
            <option value="created_at">Created Date</option>
            <option value="updated_at">Updated Date</option>
            <option value="due_datetime">Due Date</option>
            <option value="priority">Priority</option>
            <option value="title">Title</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Order</label>
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value as 'asc' | 'desc')}
            className="w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
          >
            <option value="desc">Descending</option>
            <option value="asc">Ascending</option>
          </select>
        </div>
      </div>

      <div className="mt-4 flex justify-end">
        <button
          onClick={handleReset}
          className="text-sm font-medium text-blue-600 hover:text-blue-800"
        >
          Reset Filters
        </button>
      </div>
    </div>
  );
}