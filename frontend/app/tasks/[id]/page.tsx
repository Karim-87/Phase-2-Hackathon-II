'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Task } from '@/types/task';
import { taskService } from '@/lib/api/task-service';
import TaskForm from '@/components/tasks/task-form';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import ModernButton from '@/components/ui/modern-button';
import PriorityBadge from '@/components/tasks/priority-badge';

export default function TaskDetailPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const data = await taskService.getTaskById(taskId);
        setTask(data);
      } catch {
        router.push('/tasks');
      } finally {
        setLoading(false);
      }
    };
    fetchTask();
  }, [taskId, router]);

  const handleUpdate = (updatedTask: Task) => {
    setTask(updatedTask);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await taskService.deleteTask(taskId);
      router.push('/dashboard');
    } catch {
      setIsDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!task) return null;

  if (isEditing) {
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 py-6">
        <div className="modern-card p-6 sm:p-8">
          <h1 className="text-xl sm:text-2xl font-bold text-[rgb(var(--text-primary))] mb-6">Edit Task</h1>
          <TaskForm task={task} onSubmit={handleUpdate} onCancel={() => setIsEditing(false)} />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-6">
      <div className="modern-card p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <h1 className={`text-xl sm:text-2xl font-bold ${task.is_completed ? 'line-through text-gray-400' : 'text-[rgb(var(--text-primary))]'}`}>
            {task.title}
          </h1>
          <PriorityBadge priority={task.priority} />
        </div>

        {task.description && (
          <p className="text-[rgb(var(--text-secondary))] mb-6">{task.description}</p>
        )}

        {task.due_datetime && (
          <p className="text-sm text-gray-500 mb-6">
            Due: {new Date(task.due_datetime).toLocaleString()}
          </p>
        )}

        <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-100">
          <ModernButton variant="primary" onClick={() => setIsEditing(true)} className="flex-1">
            Edit
          </ModernButton>
          <ModernButton variant="danger" onClick={() => setShowDeleteConfirm(true)} className="flex-1">
            Delete
          </ModernButton>
          <ModernButton variant="secondary" onClick={() => router.push('/dashboard')} className="flex-1">
            Back
          </ModernButton>
        </div>
      </div>

      {showDeleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
          <div className="modern-card p-6 max-w-sm w-full">
            <h3 className="text-lg font-semibold text-[rgb(var(--text-primary))] mb-2">Delete Task?</h3>
            <p className="text-sm text-[rgb(var(--text-secondary))] mb-6">
              This action cannot be undone. The task will be permanently deleted.
            </p>
            <div className="flex gap-3">
              <ModernButton variant="danger" isLoading={isDeleting} onClick={handleDelete} className="flex-1">
                Delete
              </ModernButton>
              <ModernButton variant="secondary" onClick={() => setShowDeleteConfirm(false)} className="flex-1">
                Cancel
              </ModernButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
