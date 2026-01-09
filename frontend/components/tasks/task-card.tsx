import { Task } from '@/types/task';
import Link from 'next/link';
import PriorityBadge from '@/components/tasks/priority-badge';

interface TaskCardProps {
  task: Task;
  onDelete: (id: string) => void;
  onToggleComplete: (id: string) => void;
}

export default function TaskCard({ task, onDelete, onToggleComplete }: TaskCardProps) {
  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this task?')) {
      onDelete(task.id);
    }
  };

  const handleToggleComplete = () => {
    onToggleComplete(task.id);
  };

  return (
    <div
      className={`p-4 rounded-lg shadow border-l-4 ${
        task.is_completed
          ? 'bg-gray-100 border-gray-400 opacity-75'
          : task.priority === 'urgent_important'
            ? 'bg-red-50 border-red-500'
            : task.priority === 'urgent_not_important'
              ? 'bg-orange-50 border-orange-500'
              : task.priority === 'not_urgent_important'
                ? 'bg-yellow-50 border-yellow-500'
                : 'bg-gray-50 border-gray-400'
      }`}
    >
      <div className="flex justify-between items-start">
        <div className="flex-1 min-w-0">
          <Link href={`/tasks/${task.id}`} className="block">
            <h3
              className={`font-semibold truncate ${
                task.is_completed ? 'line-through text-gray-500' : 'text-gray-800 hover:underline'
              }`}
            >
              {task.title}
            </h3>
          </Link>
          {task.description && (
            <p
              className={`mt-1 text-sm truncate ${
                task.is_completed ? 'line-through text-gray-500' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}
        </div>
        <div className="ml-4 flex-shrink-0">
          <button
            onClick={handleToggleComplete}
            className={`p-1 rounded-full ${
              task.is_completed
                ? 'text-green-600 hover:bg-green-100'
                : 'text-gray-400 hover:bg-gray-200'
            }`}
            aria-label={task.is_completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {task.is_completed ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </button>
        </div>
      </div>

      <div className="mt-3 flex flex-wrap items-center justify-between gap-2">
        <PriorityBadge priority={task.priority} />

        {task.due_datetime && (
          <div className="text-xs text-gray-500 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {new Date(task.due_datetime).toLocaleDateString()}
          </div>
        )}

        <div className="flex space-x-2">
          <Link
            href={`/tasks/${task.id}`}
            className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200"
          >
            Edit
          </Link>
          <button
            onClick={handleDelete}
            className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded hover:bg-red-200"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}