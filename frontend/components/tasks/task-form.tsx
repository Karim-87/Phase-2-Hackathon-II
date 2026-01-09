'use client';

import { useState } from 'react';
import { Task, CreateTaskData, UpdateTaskData, PriorityLevel } from '@/types/task';
import { taskService } from '@/lib/api/task-service';

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

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
    } catch (err) {
      setError(isEditing ? 'Failed to update task' : 'Failed to create task');
      console.error('Task form error:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Task title"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Task description"
        />
      </div>

      <div>
        <label htmlFor="dueDateTime" className="block text-sm font-medium text-gray-700">
          Due Date & Time
        </label>
        <input
          type="datetime-local"
          id="dueDateTime"
          value={dueDateTime}
          onChange={(e) => setDueDateTime(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="priority" className="block text-sm font-medium text-gray-700">
          Priority
        </label>
        <select
          id="priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value as PriorityLevel)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option value="urgent_important">Urgent & Important</option>
          <option value="urgent_not_important">Urgent & Not Important</option>
          <option value="not_urgent_important">Not Urgent & Important</option>
          <option value="not_urgent_not_important">Not Urgent & Not Important</option>
        </select>
      </div>

      {isEditing && (
        <div className="flex items-center">
          <input
            id="isCompleted"
            type="checkbox"
            checked={isCompleted}
            onChange={(e) => setIsCompleted(e.target.checked)}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label htmlFor="isCompleted" className="ml-2 block text-sm text-gray-700">
            Mark as completed
          </label>
        </div>
      )}

      <div className="flex space-x-3">
        <button
          type="submit"
          className="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          {isEditing ? 'Update Task' : 'Create Task'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}