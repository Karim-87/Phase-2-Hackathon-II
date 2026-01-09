'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Task } from '@/types/task';
import { taskService } from '@/lib/api/task-service';
import TaskForm from '@/components/tasks/task-form';

export default function TaskDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (id) {
      fetchTask();
    }
  }, [id]);

  const fetchTask = async () => {
    try {
      setLoading(true);
      const taskData = await taskService.getTaskById(id as string);
      setTask(taskData);
    } catch (error) {
      console.error('Failed to fetch task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdate = async (updatedTask: Task) => {
    setTask(updatedTask);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      try {
        await taskService.deleteTask(id as string);
        router.push('/dashboard');
      } catch (error) {
        console.error('Failed to delete task:', error);
      }
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[80vh]">
        <p>Loading task...</p>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="flex justify-center items-center min-h-[80vh]">
        <p>Task not found.</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          {isEditing ? 'Edit Task' : 'Task Details'}
        </h1>
        <div className="flex space-x-3">
          {!isEditing ? (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Delete
              </button>
            </>
          ) : (
            <button
              onClick={handleCancelEdit}
              className="py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
          )}
        </div>
      </div>

      {isEditing ? (
        <TaskForm
          task={task}
          onSubmit={handleTaskUpdate}
          onCancel={handleCancelEdit}
        />
      ) : (
        <div className="space-y-4">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">{task.title}</h2>
          </div>

          {task.description && (
            <div>
              <h3 className="text-sm font-medium text-gray-700">Description</h3>
              <p className="mt-1 text-gray-600">{task.description}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            {task.due_datetime && (
              <div>
                <h3 className="text-sm font-medium text-gray-700">Due Date & Time</h3>
                <p className="mt-1 text-gray-600">
                  {new Date(task.due_datetime).toLocaleString()}
                </p>
              </div>
            )}

            <div>
              <h3 className="text-sm font-medium text-gray-700">Priority</h3>
              <div className="mt-1">
                <span
                  className={`text-xs px-2 py-1 rounded ${
                    task.priority === 'urgent_important'
                      ? 'bg-red-600 text-white'
                      : task.priority === 'urgent_not_important'
                        ? 'bg-orange-600 text-white'
                        : task.priority === 'not_urgent_important'
                          ? 'bg-yellow-600 text-white'
                          : 'bg-gray-600 text-white'
                  }`}
                >
                  {task.priority.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-700">Status</h3>
              <p className={`mt-1 ${task.is_completed ? 'text-green-600' : 'text-gray-600'}`}>
                {task.is_completed ? 'Completed' : 'Pending'}
              </p>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-700">Created</h3>
              <p className="mt-1 text-gray-600">
                {new Date(task.created_at).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}