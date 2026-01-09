export interface Task {
  id: string;
  title: string;
  description?: string;
  due_datetime?: string;
  priority: 'urgent_important' | 'urgent_not_important' | 'not_urgent_important' | 'not_urgent_not_important';
  is_completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export type PriorityLevel =
  | 'urgent_important'
  | 'urgent_not_important'
  | 'not_urgent_important'
  | 'not_urgent_not_important';

export interface CreateTaskData {
  title: string;
  description?: string;
  due_datetime?: string;
  priority: PriorityLevel;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  due_datetime?: string;
  priority?: PriorityLevel;
  is_completed?: boolean;
}