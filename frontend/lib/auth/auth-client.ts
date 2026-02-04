import { UserSession } from '@/types/user';

class AuthClient {
  private tokenKey = 'jwt_token';

  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  removeToken(): void {
    localStorage.removeItem(this.tokenKey);
  }

  // Parse JWT token to extract user info
  parseToken(token: string): { userId: string; email?: string; name?: string; exp: number } | null {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      const payload = JSON.parse(jsonPayload);
      return {
        userId: payload.user_id || '',  // Backend sends 'user_id', not 'userId'
        email: payload.email || '',
        name: payload.name || '',
        exp: payload.exp || 0,
      };
    } catch (e) {
      console.error('Failed to parse JWT:', e);
      return null;
    }
  }

  isTokenExpired(token: string): boolean {
    const parsed = this.parseToken(token);
    if (!parsed) return true;

    return parsed.exp * 1000 < Date.now();
  }

  getUserFromToken(): UserSession | null {
    const token = this.getToken();
    if (!token || this.isTokenExpired(token)) {
      return null;
    }

    const parsed = this.parseToken(token);
    if (!parsed) {
      return null;
    }

    return {
      jwt_token: token,
      user_id: parsed.userId,
      expires_at: new Date(parsed.exp * 1000).toISOString(),
      is_authenticated: true,
    };
  }
}

export const authClient = new AuthClient();