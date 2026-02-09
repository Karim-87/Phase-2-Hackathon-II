import { useState, useEffect, useCallback } from 'react';
import { Task, CreateTaskData, UpdateTaskData, PriorityLevel } from '@/types/task';
import { taskService } from '@/lib/api/task-service';

interface FilterParams {
  priority?: PriorityLevel;
  is_completed?: boolean;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [currentFilters, setCurrentFilters] = useState<FilterParams>({});

  const fetchTasks = useCallback(async (filters?: FilterParams) => {
    try {
      setLoading(true);
      setError(null);
      const params = filters || currentFilters;
      const result = await taskService.getTasksWithFilters({
        priority: params.priority,
        is_completed: params.is_completed,
        sort_by: params.sort_by,
        sort_order: params.sort_order,
      });
      setTasks(result.tasks);
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err
        ? (err as { message: string }).message
        : 'Failed to fetch tasks';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [currentFilters]);

  const createTask = async (taskData: CreateTaskData) => {
    try {
      setIsCreating(true);
      setError(null);
      const newTask = await taskService.createTask(taskData);
      setTasks(prev => [newTask, ...prev]);
      return newTask;
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err
        ? (err as { message: string }).message
        : 'Failed to create task';
      setError(message);
      throw err;
    } finally {
      setIsCreating(false);
    }
  };

  const updateTask = async (id: string, taskData: UpdateTaskData) => {
    try {
      setIsUpdating(true);
      setError(null);
      const updatedTask = await taskService.updateTask(id, taskData);
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      return updatedTask;
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err
        ? (err as { message: string }).message
        : 'Failed to update task';
      setError(message);
      throw err;
    } finally {
      setIsUpdating(false);
    }
  };

  const deleteTask = async (id: string) => {
    try {
      setIsDeleting(true);
      setError(null);
      await taskService.deleteTask(id);
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err
        ? (err as { message: string }).message
        : 'Failed to delete task';
      setError(message);
      throw err;
    } finally {
      setIsDeleting(false);
    }
  };

  const toggleTaskCompletion = async (id: string) => {
    try {
      setIsUpdating(true);
      setError(null);
      const task = tasks.find(t => t.id === id);
      if (!task) throw new Error('Task not found');

      const updatedTask = await taskService.toggleTaskCompletion(id, !task.is_completed);
      setTasks(prev => prev.map(t => t.id === id ? updatedTask : t));
      return updatedTask;
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err
        ? (err as { message: string }).message
        : 'Failed to toggle task completion';
      setError(message);
      throw err;
    } finally {
      setIsUpdating(false);
    }
  };

  const applyFilters = useCallback((params: {
    priority?: PriorityLevel;
    completed?: boolean;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    const filters: FilterParams = {
      priority: params.priority,
      is_completed: params.completed,
      sort_by: params.sortBy,
      sort_order: params.sortOrder,
    };
    setCurrentFilters(filters);
    fetchTasks(filters);
  }, [fetchTasks]);

  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    allTasks: tasks,
    loading,
    error,
    isCreating,
    isUpdating,
    isDeleting,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    applyFilters,
  };
}
