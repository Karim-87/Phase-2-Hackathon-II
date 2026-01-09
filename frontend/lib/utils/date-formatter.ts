/**
 * Formats a date string to a localized date and time string
 */
export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

/**
 * Formats a date string to a localized date string only
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

/**
 * Formats a date string to a localized time string only
 */
export const formatTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleTimeString();
};

/**
 * Checks if a date is in the past
 */
export const isPastDate = (dateString: string): boolean => {
  const date = new Date(dateString);
  return date < new Date();
};

/**
 * Checks if a date is in the future
 */
export const isFutureDate = (dateString: string): boolean => {
  const date = new Date(dateString);
  return date > new Date();
};

/**
 * Returns how much time is left until the given date in a human-readable format
 */
export const getTimeUntil = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = date.getTime() - now.getTime();

  if (diffMs < 0) {
    return 'Overdue';
  }

  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

  if (diffDays > 0) {
    return `${diffDays} day${diffDays !== 1 ? 's' : ''}`;
  } else if (diffHours > 0) {
    return `${diffHours} hour${diffHours !== 1 ? 's' : ''}`;
  } else {
    return `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''}`;
  }
};

/**
 * Formats a date relative to the current time (e.g. "2 hours ago", "in 3 days")
 */
export const formatRelativeTime = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = Math.abs(now.getTime() - date.getTime());
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  const diffWeeks = Math.floor(diffDays / 7);
  const diffMonths = Math.floor(diffDays / 30);
  const diffYears = Math.floor(diffDays / 365);

  if (diffSecs < 60) {
    return 'Just now';
  } else if (diffMins < 60) {
    return date < now ? `${diffMins}m ago` : `in ${diffMins}m`;
  } else if (diffHours < 24) {
    return date < now ? `${diffHours}h ago` : `in ${diffHours}h`;
  } else if (diffDays < 7) {
    return date < now ? `${diffDays}d ago` : `in ${diffDays}d`;
  } else if (diffWeeks < 5) {
    return date < now ? `${diffWeeks}w ago` : `in ${diffWeeks}w`;
  } else if (diffMonths < 12) {
    return date < now ? `${diffMonths}mo ago` : `in ${diffMonths}mo`;
  } else {
    return date < now ? `${diffYears}y ago` : `in ${diffYears}y`;
  }
};