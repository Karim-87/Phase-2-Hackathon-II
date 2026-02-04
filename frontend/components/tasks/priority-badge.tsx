import { PriorityLevel } from '@/types/task';

interface PriorityBadgeProps {
  priority: PriorityLevel;
}

export default function PriorityBadge({ priority }: PriorityBadgeProps) {
  const getPriorityClass = () => {
    switch (priority) {
      case 'urgent_important':
        return 'priority-urgent-important';
      case 'urgent_not_important':
        return 'priority-urgent-not-important';
      case 'not_urgent_important':
        return 'priority-not-urgent-important';
      case 'not_urgent_not_important':
        return 'priority-not-urgent-not-important';
      default:
        return 'priority-not-urgent-not-important';
    }
  };

  const getPriorityText = () => {
    switch (priority) {
      case 'urgent_important':
        return 'Do First';
      case 'urgent_not_important':
        return 'Delegate';
      case 'not_urgent_important':
        return 'Schedule';
      case 'not_urgent_not_important':
        return 'Eliminate';
      default:
        return priority;
    }
  };

  return (
    <span
      className={`priority-badge ${getPriorityClass()}`}
      role="status"
      aria-label={`Priority: ${getPriorityText()}`}
    >
      {getPriorityText()}
    </span>
  );
}