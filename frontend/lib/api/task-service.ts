import { Task, CreateTaskData, UpdateTaskData, PriorityLevel } from '@/types/task';
import { apiClient } from './api-client';

interface ApiResponse<T> {
  success: boolean;
  data: T;
}

interface TaskListResponse {
  tasks: Task[];
  total_count: number;
  limit: number;
  offset: number;
}

class TaskService {
  async getAllTasks(): Promise<Task[]> {
    const response = await apiClient.get<ApiResponse<TaskListResponse>>('/api/tasks');
    return response.data?.tasks || [];
  }

  async getTaskById(id: string): Promise<Task> {
    const response = await apiClient.get<ApiResponse<Task>>(`/api/tasks/${id}`);
    return response.data;
  }

  async createTask(data: CreateTaskData): Promise<Task> {
    const response = await apiClient.post<ApiResponse<Task>>('/api/tasks', data);
    return response.data;
  }

  async updateTask(id: string, data: UpdateTaskData): Promise<Task> {
    const response = await apiClient.put<ApiResponse<Task>>(`/api/tasks/${id}`, data);
    return response.data;
  }

  async deleteTask(id: string): Promise<void> {
    await apiClient.delete<void>(`/api/tasks/${id}`);
  }

  async toggleTaskCompletion(id: string, isCompleted?: boolean): Promise<Task> {
    const response = await apiClient.patch<ApiResponse<Task>>(`/api/tasks/${id}/complete`, { completed: isCompleted });
    return response.data;
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

    const response = await apiClient.get<ApiResponse<TaskListResponse>>(endpoint);
    return response.data?.tasks || [];
  }
}

export const taskService = new TaskService();