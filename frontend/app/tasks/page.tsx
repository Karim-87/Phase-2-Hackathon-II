'use client';

import { useState, useEffect } from 'react';
import { useTasks } from '@/hooks/use-tasks';
import { useAuth } from '@/components/auth/auth-provider';
import { PriorityLevel } from '@/types/task';
import Link from 'next/link';
import TaskFilters from '@/components/tasks/task-filters';
import TaskList from '@/components/tasks/task-list';
import ModernButton from '@/components/ui/modern-button';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { Toast, useToast } from '@/components/ui/toast';

interface FilterParams {
  priority: PriorityLevel | undefined;
  completed: boolean | undefined;
  sortBy: string;
  sortOrder: 'asc' | 'desc';
}

export default function TasksPage() {
  const { tasks, loading, error, applyFilters } = useTasks();
  const { user, isLoading: authLoading } = useAuth();
  const { toasts, addToast, dismissToast } = useToast();
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

  useEffect(() => {
    if (error) {
      addToast(error, 'error');
    }
  }, [error, addToast]);

  if (authLoading) {
    return (
      <div className="flex justify-center items-center min-h-[80vh]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-[80vh] px-4">
        <p className="text-[rgb(var(--text-secondary))]">Please sign in to view your tasks.</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <Toast toasts={toasts} onDismiss={dismissToast} />
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 sm:mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-[rgb(var(--text-primary))]">All Tasks</h1>
        <Link href="/tasks/create">
          <ModernButton variant="primary">
            Create Task
          </ModernButton>
        </Link>
      </div>

      <TaskFilters onFilterChange={handleFilterChange} />

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-100 text-red-600 rounded-xl flex items-center gap-2">
          <svg className="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          <span className="text-sm">{error}</span>
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      ) : (
        <TaskList initialTasks={tasks} />
      )}

      {tasks.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-[rgb(var(--text-secondary))] text-base sm:text-lg">No tasks found. Create your first task!</p>
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
