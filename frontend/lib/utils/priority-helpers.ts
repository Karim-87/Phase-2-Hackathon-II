import { PriorityLevel } from '@/types/task';

/**
 * Maps priority levels to their corresponding CSS classes for styling
 */
export const getPriorityClass = (priority: PriorityLevel): string => {
  switch (priority) {
    case 'urgent_important':
      return 'priority-urgent-important bg-red-600 text-white';
    case 'urgent_not_important':
      return 'priority-urgent-not-important bg-orange-600 text-white';
    case 'not_urgent_important':
      return 'priority-not-urgent-important bg-yellow-600 text-white';
    case 'not_urgent_not_important':
      return 'priority-not-urgent-not-important bg-gray-600 text-white';
    default:
      return 'priority-not-urgent-not-important bg-gray-600 text-white';
  }
};

/**
 * Returns a human-readable label for the priority level
 */
export const getPriorityLabel = (priority: PriorityLevel): string => {
  switch (priority) {
    case 'urgent_important':
      return 'Urgent & Important';
    case 'urgent_not_important':
      return 'Urgent & Not Important';
    case 'not_urgent_important':
      return 'Not Urgent & Important';
    case 'not_urgent_not_important':
      return 'Not Urgent & Not Important';
    default:
      return priority;
  }
};

/**
 * Returns a color code for the priority level (used for styling)
 */
export const getPriorityColor = (priority: PriorityLevel): string => {
  switch (priority) {
    case 'urgent_important':
      return '#dc2626'; // red-600
    case 'urgent_not_important':
      return '#ea580c'; // orange-600
    case 'not_urgent_important':
      return '#ca8a04'; // yellow-600
    case 'not_urgent_not_important':
      return '#64748b'; // slate-500
    default:
      return '#64748b'; // slate-500
  }
};

/**
 * Sorts tasks by priority level based on the Eisenhower Matrix
 * (urgent_important first, then not_urgent_important, then urgent_not_important, then not_urgent_not_important)
 */
export const sortTasksByPriority = (tasks: any[]): any[] => {
  const priorityOrder: Record<PriorityLevel, number> = {
    urgent_important: 1,
    not_urgent_important: 2,
    urgent_not_important: 3,
    not_urgent_not_important: 4,
  };

  return [...tasks].sort((a, b) => {
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
};

/**
 * Filters tasks by priority level
 */
export const filterTasksByPriority = (tasks: any[], priority: PriorityLevel): any[] => {
  return tasks.filter((task) => task.priority === priority);
};