export interface ApiError {
  message: string;
  code?: string;
  status: number;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || '';
  }

  async request<T = unknown>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const token = typeof window !== 'undefined' ? localStorage.getItem('jwt_token') : null;

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);

    const config: RequestInit = {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      clearTimeout(timeout);

      if (response.status === 401) {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('jwt_token');
          document.cookie = 'jwt_token=; path=/; max-age=0';
          window.location.href = '/sign-in';
        }
        throw { message: 'Session expired. Please sign in again.', code: 'TOKEN_EXPIRED', status: 401 } as ApiError;
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw {
          message: errorData.error || errorData.detail || `Request failed (${response.status})`,
          code: errorData.error_code,
          status: response.status,
        } as ApiError;
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeout);
      if (error && typeof error === 'object' && 'status' in error) {
        throw error;
      }
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw { message: 'Request timed out', code: 'TIMEOUT', status: 0 } as ApiError;
      }
      throw { message: 'Network error. Please check your connection.', code: 'NETWORK_ERROR', status: 0 } as ApiError;
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
