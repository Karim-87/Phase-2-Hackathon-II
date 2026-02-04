'use client';

import { useState } from 'react';
import { useTasks } from '@/hooks/use-tasks';
import { useAuth } from '@/components/auth/auth-provider';
import { PriorityLevel } from '@/types/task';
import Link from 'next/link';
import TaskFilters from '@/components/tasks/task-filters';
import TaskList from '@/components/tasks/task-list';
import ModernButton from '@/components/ui/modern-button';

interface FilterParams {
  priority: PriorityLevel | undefined;
  completed: boolean | undefined;
  sortBy: string;
  sortOrder: 'asc' | 'desc';
}

export default function TasksPage() {
  const { tasks, loading, error, applyFilters } = useTasks();
  const { user, isLoading: authLoading } = useAuth();
  const [filterParams, setFilterParams] = useState<FilterParams>({
    priority: undefined,
    completed: undefined,
    sortBy: 'created_at',
    sortOrder: 'desc',
  });

  const handleFilterChange = (newFilters: {
    priority?: string;
    completed?: boolean;
    sortBy?: string;
    sortOrder?: string;
  }) => {
    const updatedFilters: FilterParams = {
      priority: newFilters.priority as PriorityLevel | undefined,
      completed: newFilters.completed,
      sortBy: newFilters.sortBy || 'created_at',
      sortOrder: (newFilters.sortOrder as 'asc' | 'desc') || 'desc',
    };
    setFilterParams(updatedFilters);
    applyFilters({
      priority: newFilters.priority as PriorityLevel | undefined,
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
        <h1 className="text-3xl font-bold text-[rgb(var(--text-primary))]">All Tasks</h1>
        <Link href="/tasks/create">
          <ModernButton variant="primary">
            Create Task
          </ModernButton>
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
          <p className="text-[rgb(var(--text-secondary))] text-lg">No tasks found. Create your first task!</p>
          <Link href="/tasks/create">
            <ModernButton variant="primary" className="mt-4">
              Create Task
            </ModernButton>
          </Link>
        </div>
      )}
    </div>
  );
}