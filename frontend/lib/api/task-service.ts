import { Task, CreateTaskData, UpdateTaskData, PriorityLevel } from '@/types/task';
import { apiClient } from './api-client';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

interface TaskListData {
  tasks: Task[];
  total_count: number;
  limit: number;
  offset: number;
}

class TaskService {
  async getAllTasks(): Promise<Task[]> {
    const response = await apiClient.get<ApiResponse<TaskListData>>('/api/v1/tasks');
    return response.data?.tasks || [];
  }

  async getTaskById(id: string): Promise<Task> {
    const response = await apiClient.get<ApiResponse<Task>>(`/api/v1/tasks/${id}`);
    return response.data;
  }

  async createTask(data: CreateTaskData): Promise<Task> {
    const response = await apiClient.post<ApiResponse<Task>>('/api/v1/tasks', data);
    return response.data;
  }

  async updateTask(id: string, data: UpdateTaskData): Promise<Task> {
    const response = await apiClient.patch<ApiResponse<Task>>(`/api/v1/tasks/${id}`, data);
    return response.data;
  }

  async deleteTask(id: string): Promise<void> {
    await apiClient.delete<ApiResponse<null>>(`/api/v1/tasks/${id}`);
  }

  async toggleTaskCompletion(id: string, isCompleted: boolean): Promise<Task> {
    const response = await apiClient.patch<ApiResponse<Task>>(`/api/v1/tasks/${id}`, {
      is_completed: isCompleted,
    });
    return response.data;
  }

  async getTasksWithFilters(params: {
    priority?: PriorityLevel;
    is_completed?: boolean;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
    limit?: number;
    offset?: number;
  }): Promise<{ tasks: Task[]; total_count: number }> {
    const searchParams = new URLSearchParams();
    if (params.priority) searchParams.append('priority', params.priority);
    if (params.is_completed !== undefined) searchParams.append('is_completed', params.is_completed.toString());
    if (params.sort_by) searchParams.append('sort_by', params.sort_by);
    if (params.sort_order) searchParams.append('sort_order', params.sort_order);
    if (params.limit) searchParams.append('limit', params.limit.toString());
    if (params.offset) searchParams.append('offset', params.offset.toString());

    const queryString = searchParams.toString();
    const endpoint = queryString ? `/api/v1/tasks?${queryString}` : '/api/v1/tasks';

    const response = await apiClient.get<ApiResponse<TaskListData>>(endpoint);
    return {
      tasks: response.data?.tasks || [],
      total_count: response.data?.total_count || 0,
    };
  }
}

export const taskService = new TaskService();
