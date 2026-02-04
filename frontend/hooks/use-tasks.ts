import { useState, useEffect } from 'react';
import { Task, CreateTaskData, UpdateTaskData, PriorityLevel } from '@/types/task';
import { taskService } from '@/lib/api/task-service';

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch all tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const tasksData = await taskService.getAllTasks();
      setTasks(tasksData);
      setFilteredTasks(tasksData);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Create a new task
  const createTask = async (taskData: CreateTaskData) => {
    try {
      const newTask = await taskService.createTask(taskData);
      setTasks(prev => [newTask, ...prev]);
      setFilteredTasks(prev => [newTask, ...prev]);
      return newTask;
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
      throw err;
    }
  };

  // Update an existing task
  const updateTask = async (id: string, taskData: UpdateTaskData) => {
    try {
      const updatedTask = await taskService.updateTask(id, taskData);
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      setFilteredTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      return updatedTask;
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
      throw err;
    }
  };

  // Delete a task
  const deleteTask = async (id: string) => {
    try {
      await taskService.deleteTask(id);
      setTasks(prev => prev.filter(task => task.id !== id));
      setFilteredTasks(prev => prev.filter(task => task.id !== id));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
      throw err;
    }
  };

  // Toggle task completion
  const toggleTaskCompletion = async (id: string) => {
    try {
      const task = tasks.find(t => t.id === id);
      if (!task) throw new Error('Task not found');

      const updatedTask = await taskService.toggleTaskCompletion(id, !task.is_completed);
      setTasks(prev => prev.map(t => t.id === id ? updatedTask : t));
      setFilteredTasks(prev => prev.map(t => t.id === id ? updatedTask : t));
      return updatedTask;
    } catch (err) {
      setError('Failed to toggle task completion');
      console.error('Error toggling task completion:', err);
      throw err;
    }
  };

  // Apply filters to tasks
  const applyFilters = (params: {
    priority?: PriorityLevel;
    completed?: boolean;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    let filtered = [...tasks];

    // Apply priority filter
    if (params.priority) {
      filtered = filtered.filter(task => task.priority === params.priority);
    }

    // Apply completion filter
    if (params.completed !== undefined) {
      filtered = filtered.filter(task => task.is_completed === params.completed);
    }

    // Apply sorting
    const sortBy = params.sortBy;
    if (sortBy) {
      filtered.sort((a, b) => {
        // Get the values to compare
        let valA: any = a[sortBy as keyof Task];
        let valB: any = b[sortBy as keyof Task];

        // Handle date comparison
        if (sortBy.includes('_datetime') || sortBy.includes('_at')) {
          valA = new Date(valA);
          valB = new Date(valB);
        }

        // Handle string comparison
        if (typeof valA === 'string' && typeof valB === 'string') {
          valA = valA.toLowerCase();
          valB = valB.toLowerCase();
        }

        // Compare values
        if (valA < valB) {
          return params.sortOrder === 'asc' ? -1 : 1;
        }
        if (valA > valB) {
          return params.sortOrder === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }

    setFilteredTasks(filtered);
  };

  // Initialize tasks on mount
  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks: filteredTasks,
    allTasks: tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    applyFilters,
  };
}