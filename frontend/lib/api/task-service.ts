import { Task, CreateTaskData, UpdateTaskData } from '@/types/task';
import { apiClient } from './api-client';

class TaskService {
  async getAllTasks(): Promise<Task[]> {
    return apiClient.get<Task[]>('/api/tasks');
  }

  async getTaskById(id: string): Promise<Task> {
    return apiClient.get<Task>(`/api/tasks/${id}`);
  }

  async createTask(data: CreateTaskData): Promise<Task> {
    return apiClient.post<Task>('/api/tasks', data);
  }

  async updateTask(id: string, data: UpdateTaskData): Promise<Task> {
    return apiClient.put<Task>(`/api/tasks/${id}`, data);
  }

  async deleteTask(id: string): Promise<void> {
    return apiClient.delete<void>(`/api/tasks/${id}`);
  }

  async toggleTaskCompletion(id: string, isCompleted?: boolean): Promise<Task> {
    return apiClient.patch<Task>(`/api/tasks/${id}/complete`, { is_completed: isCompleted });
  }

  async getTasksWithFilters(
    priority?: PriorityLevel,
    completed?: boolean,
    sortBy?: string,
    sortOrder?: 'asc' | 'desc'
  ): Promise<Task[]> {
    const params = new URLSearchParams();
    if (priority) params.append('priority', priority);
    if (completed !== undefined) params.append('completed', completed.toString());
    if (sortBy) params.append('sortBy', sortBy);
    if (sortOrder) params.append('sortOrder', sortOrder);

    const queryString = params.toString();
    const endpoint = queryString ? `/api/tasks?${queryString}` : '/api/tasks';

    return apiClient.get<Task[]>(endpoint);
  }
}

export const taskService = new TaskService();