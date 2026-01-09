'use client';

import { useRouter } from 'next/navigation';
import TaskForm from '@/components/tasks/task-form';
import { Task } from '@/types/task';

export default function CreateTaskPage() {
  const router = useRouter();

  const handleTaskSubmit = (task: Task) => {
    // Redirect to dashboard after creating task
    router.push('/dashboard');
  };

  const handleCancel = () => {
    // Go back to dashboard
    router.push('/dashboard');
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Create New Task</h1>
      <TaskForm onSubmit={handleTaskSubmit} onCancel={handleCancel} />
    </div>
  );
}