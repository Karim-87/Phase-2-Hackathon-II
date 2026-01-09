import { PriorityLevel } from '@/types/task';

interface PriorityBadgeProps {
  priority: PriorityLevel;
}

export default function PriorityBadge({ priority }: PriorityBadgeProps) {
  const getPriorityClass = () => {
    switch (priority) {
      case 'urgent_important':
        return 'bg-red-600 text-white';
      case 'urgent_not_important':
        return 'bg-orange-600 text-white';
      case 'not_urgent_important':
        return 'bg-yellow-600 text-white';
      case 'not_urgent_not_important':
        return 'bg-gray-600 text-white';
      default:
        return 'bg-gray-600 text-white';
    }
  };

  const getPriorityText = () => {
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

  return (
    <span className={`text-xs px-2 py-1 rounded ${getPriorityClass()}`}>
      {getPriorityText()}
    </span>
  );
}