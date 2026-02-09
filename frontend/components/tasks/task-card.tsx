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

  return (
    <div
      className={`flex items-center gap-4 py-4 px-2 ${
        task.is_completed ? 'opacity-60' : ''
      }`}
    >
      {/* Toggle button */}
      <button
        onClick={() => onToggleComplete(task.id)}
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 ${
          task.is_completed
            ? 'bg-emerald-500 text-white'
            : 'border-2 border-gray-300 text-transparent hover:border-indigo-400 hover:text-indigo-400'
        }`}
        aria-label={task.is_completed ? 'Mark incomplete' : 'Mark complete'}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path
            fillRule="evenodd"
            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {/* Title + description */}
      <div className="flex-1 min-w-0">
        <Link href={`/tasks/${task.id}`} className="group">
          <span
            className={`text-sm sm:text-base font-medium transition-colors truncate block ${
              task.is_completed
                ? 'line-through text-gray-400'
                : 'text-gray-800 group-hover:text-indigo-600'
            }`}
          >
            {task.title}
          </span>
        </Link>
        {task.description && (
          <p
            className={`text-xs truncate mt-0.5 ${
              task.is_completed ? 'line-through text-gray-400' : 'text-gray-500'
            }`}
          >
            {task.description}
          </p>
        )}
      </div>

      {/* Priority + due date */}
      <div className="flex items-center gap-2 flex-shrink-0">
        <PriorityBadge priority={task.priority} />
        {task.due_datetime && (
          <span className="text-xs text-gray-400">
            {new Date(task.due_datetime).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
          </span>
        )}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-1 flex-shrink-0">
        <Link href={`/tasks/${task.id}`}>
          <button className="px-2 py-1 text-xs font-medium text-gray-500 hover:text-indigo-600 transition-colors">
            Edit
          </button>
        </Link>
        <button
          onClick={handleDelete}
          className="px-2 py-1 text-xs font-medium text-gray-400 hover:text-red-600 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
