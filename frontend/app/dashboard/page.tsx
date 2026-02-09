'use client';

import { useState } from 'react';
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

export default function DashboardPage() {
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
        <p className="text-[rgb(var(--text-secondary))]">Please sign in to view your dashboard.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Toast toasts={toasts} onDismiss={dismissToast} />

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content animate-fade-in px-4">
          <h1 className="hero-title bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent text-2xl sm:text-3xl md:text-4xl">
            Your Tasks
          </h1>
          <p className="hero-subtitle text-sm sm:text-base">Manage your tasks efficiently with our Eisenhower Matrix approach</p>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Action Bar */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 sm:mb-8">
          <div>
            <h2 className="text-lg sm:text-xl font-semibold text-gray-800">All Tasks</h2>
            <p className="text-sm text-gray-500">{tasks.length} task{tasks.length !== 1 ? 's' : ''} total</p>
          </div>
          <Link href="/tasks/create">
            <ModernButton variant="primary">
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create Task
              </span>
            </ModernButton>
          </Link>
        </div>

        <TaskFilters onFilterChange={handleFilterChange} />

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-100 text-red-600 rounded-xl flex items-center gap-2">
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
          <div className="text-center py-12 sm:py-16">
            <div className="mx-auto w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl flex items-center justify-center mb-4 sm:mb-6">
              <svg className="w-8 h-8 sm:w-10 sm:h-10 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-lg sm:text-xl font-semibold text-gray-800 mb-2">No tasks yet</h3>
            <p className="text-gray-500 mb-6 text-sm sm:text-base">Create your first task to get started!</p>
            <Link href="/tasks/create">
              <ModernButton variant="primary">
                <span className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Create Task
                </span>
              </ModernButton>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
