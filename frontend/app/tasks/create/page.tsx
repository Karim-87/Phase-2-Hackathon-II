'use client';

import { useRouter } from 'next/navigation';
import TaskForm from '@/components/tasks/task-form';
import { Task } from '@/types/task';

export default function CreateTaskPage() {
  const router = useRouter();

  const handleTaskSubmit = (task: Task) => {
    router.push('/dashboard');
  };

  const handleCancel = () => {
    router.push('/dashboard');
  };

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-6">
      <div className="modern-card p-6 sm:p-8">
        <h1 className="text-xl sm:text-2xl font-bold text-[rgb(var(--text-primary))] mb-6">Create New Task</h1>
        <TaskForm onSubmit={handleTaskSubmit} onCancel={handleCancel} />
      </div>
    </div>
  );
}
