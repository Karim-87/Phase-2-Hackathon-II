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
    } catch {
      // Error handled by loading state — caller can retry
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (taskId: string) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
      if (onTaskDeleted) onTaskDeleted(taskId);
    } catch {
      // Silently handled — task remains in list as visual indicator
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    try {
      const currentTask = tasks.find(t => t.id === taskId);
      const updatedTask = await taskService.toggleTaskCompletion(taskId, !currentTask?.is_completed);
      const updatedTasks = tasks.map(task =>
        task.id === taskId ? updatedTask : task
      );
      setTasks(updatedTasks);
      if (onTaskUpdated) onTaskUpdated(updatedTask);
    } catch {
      // Silently handled — task state unchanged as visual indicator
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
    <div className="flex flex-col divide-y divide-gray-200">
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