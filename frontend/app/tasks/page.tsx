'use client';

import { useState } from 'react';
import { useTasks } from '@/hooks/use-tasks';
import { useAuth } from '@/hooks/use-auth';
import Link from 'next/link';
import TaskFilters from '@/components/tasks/task-filters';
import TaskList from '@/components/tasks/task-list';

export default function TasksPage() {
  const { tasks, loading, error, applyFilters } = useTasks();
  const { user, isLoading: authLoading } = useAuth();
  const [filterParams, setFilterParams] = useState({
    priority: undefined,
    completed: undefined,
    sortBy: 'created_at',
    sortOrder: 'desc' as const,
  });

  const handleFilterChange = (newFilters: {
    priority?: string;
    completed?: boolean;
    sortBy?: string;
    sortOrder?: string;
  }) => {
    setFilterParams({
      priority: newFilters.priority,
      completed: newFilters.completed,
      sortBy: newFilters.sortBy || 'created_at',
      sortOrder: (newFilters.sortOrder as 'asc' | 'desc') || 'desc',
    });
    applyFilters({
      priority: newFilters.priority,
      completed: newFilters.completed,
      sortBy: newFilters.sortBy,
      sortOrder: newFilters.sortOrder as 'asc' | 'desc',
    });
  };

  if (authLoading) {
    return (
      <div className="flex justify-center items-center min-h-[80vh]">
        <p>Loading...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-[80vh]">
        <p>Please sign in to view your tasks.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">All Tasks</h1>
        <Link
          href="/tasks/create"
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
        >
          Create Task
        </Link>
      </div>

      <TaskFilters onFilterChange={handleFilterChange} />

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      <TaskList initialTasks={tasks} />

      {tasks.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No tasks found. Create your first task!</p>
          <Link
            href="/tasks/create"
            className="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Create Task
          </Link>
        </div>
      )}
    </div>
  );
}