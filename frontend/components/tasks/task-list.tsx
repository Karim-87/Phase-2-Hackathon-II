import { useState, useEffect } from 'react';
import { Task } from '@/types/task';
import TaskCard from '@/components/tasks/task-card';
import { taskService } from '@/lib/api/task-service';

interface TaskListProps {
  initialTasks?: Task[];
  onTaskUpdated?: (task: Task) => void;
  onTaskDeleted?: (taskId: string) => void;
}

export default function TaskList({ initialTasks = [], onTaskUpdated, onTaskDeleted }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [loading, setLoading] = useState(!initialTasks.length);

  useEffect(() => {
    if (!initialTasks.length) {
      loadTasks();
    }
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await taskService.getAllTasks();
      setTasks(tasksData);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (taskId: string) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
      if (onTaskDeleted) onTaskDeleted(taskId);
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    try {
      const updatedTask = await taskService.toggleTaskCompletion(taskId);
      const updatedTasks = tasks.map(task =>
        task.id === taskId ? updatedTask : task
      );
      setTasks(updatedTasks);
      if (onTaskUpdated) onTaskUpdated(updatedTask);
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <p>Loading tasks...</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No tasks found.</p>
      </div>
    );
  }

  return (
    <div className="grid modern-layout-grid">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onDelete={handleDelete}
          onToggleComplete={handleToggleComplete}
        />
      ))}
    </div>
  );
}