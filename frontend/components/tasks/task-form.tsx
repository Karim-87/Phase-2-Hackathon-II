'use client';

import { useState } from 'react';
import { Task, CreateTaskData, UpdateTaskData, PriorityLevel } from '@/types/task';
import { taskService } from '@/lib/api/task-service';
import ModernButton from '@/components/ui/modern-button';

interface TaskFormProps {
  task?: Task;
  onSubmit: (task: Task) => void;
  onCancel: () => void;
}

export default function TaskForm({ task, onSubmit, onCancel }: TaskFormProps) {
  const isEditing = !!task;

  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [dueDateTime, setDueDateTime] = useState(task?.due_datetime || '');
  const [priority, setPriority] = useState<PriorityLevel>(task?.priority || 'not_urgent_not_important');
  const [isCompleted, setIsCompleted] = useState(task?.is_completed || false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      let result: Task;

      if (isEditing && task) {
        const updateData: UpdateTaskData = {
          title: title.trim(),
          description: description.trim(),
          due_datetime: dueDateTime || undefined,
          priority,
          is_completed: isCompleted,
        };
        result = await taskService.updateTask(task.id, updateData);
      } else {
        const createData: CreateTaskData = {
          title: title.trim(),
          description: description.trim(),
          due_datetime: dueDateTime,
          priority,
        };
        result = await taskService.createTask(createData);
      }

      onSubmit(result);
    } catch {
      setError(isEditing ? 'Failed to update task' : 'Failed to create task');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-xl bg-red-50 border border-red-100 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          maxLength={255}
          className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all outline-none text-gray-900 placeholder-gray-400"
          placeholder="Task title"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          maxLength={5000}
          className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all outline-none text-gray-900 placeholder-gray-400"
          placeholder="Task description"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="dueDateTime" className="block text-sm font-medium text-gray-700 mb-1">
            Due Date & Time
          </label>
          <input
            type="datetime-local"
            id="dueDateTime"
            value={dueDateTime}
            onChange={(e) => setDueDateTime(e.target.value)}
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all outline-none text-gray-900"
          />
        </div>

        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as PriorityLevel)}
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all outline-none text-gray-900"
          >
            <option value="urgent_important">Urgent & Important</option>
            <option value="urgent_not_important">Urgent & Not Important</option>
            <option value="not_urgent_important">Not Urgent & Important</option>
            <option value="not_urgent_not_important">Not Urgent & Not Important</option>
          </select>
        </div>
      </div>

      {isEditing && (
        <div className="flex items-center">
          <input
            id="isCompleted"
            type="checkbox"
            checked={isCompleted}
            onChange={(e) => setIsCompleted(e.target.checked)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label htmlFor="isCompleted" className="ml-2 block text-sm text-gray-700">
            Mark as completed
          </label>
        </div>
      )}

      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        <ModernButton type="submit" variant="primary" isLoading={isLoading} className="flex-1">
          {isEditing ? 'Update Task' : 'Create Task'}
        </ModernButton>
        <ModernButton type="button" variant="secondary" onClick={onCancel} className="flex-1">
          Cancel
        </ModernButton>
      </div>
    </form>
  );
}
