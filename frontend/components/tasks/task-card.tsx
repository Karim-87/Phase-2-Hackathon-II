import { Task } from '@/types/task';
import Link from 'next/link';
import PriorityBadge from '@/components/tasks/priority-badge';
import ModernButton from '@/components/ui/modern-button';

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
      className={`modern-card p-6 ${
        task.is_completed ? 'opacity-60' : ''
      }`}
    >
      {/* Header with title and complete button */}
      <div className="flex justify-between items-start gap-4">
        <div className="flex-1 min-w-0">
          <Link href={`/tasks/${task.id}`} className="block group">
            <h3
              className={`text-lg font-semibold transition-colors ${
                task.is_completed
                  ? 'line-through text-gray-400'
                  : 'text-gray-800 group-hover:text-indigo-600'
              }`}
            >
              {task.title}
            </h3>
          </Link>
          {task.description && (
            <p
              className={`mt-2 text-sm line-clamp-2 ${
                task.is_completed ? 'line-through text-gray-400' : 'text-gray-500'
              }`}
            >
              {task.description}
            </p>
          )}
        </div>
        <button
          onClick={handleToggleComplete}
          className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 ${
            task.is_completed
              ? 'bg-gradient-to-r from-emerald-400 to-emerald-500 text-white shadow-lg shadow-emerald-200'
              : 'bg-gray-100 text-gray-400 hover:bg-indigo-100 hover:text-indigo-500'
          }`}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path
              fillRule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </div>

      {/* Footer with badge, date, and actions */}
      <div className="mt-4 pt-4 border-t border-gray-100 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <PriorityBadge priority={task.priority} />
          {task.due_datetime && (
            <div className="text-xs text-gray-400 flex items-center bg-gray-50 px-2 py-1 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {new Date(task.due_datetime).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Link href={`/tasks/${task.id}`}>
            <button className="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
              Edit
            </button>
          </Link>
          <button
            onClick={handleDelete}
            className="px-3 py-1.5 text-xs font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}