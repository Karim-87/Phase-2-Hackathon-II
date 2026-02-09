'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { UserSession } from '@/types/user';

interface AuthContextType {
  user: UserSession | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  signOut: () => Promise<void>;
  getToken: () => string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const parseJwt = (token: string) => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch {
      return null;
    }
  };

  const fetchProfile = async (token: string) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (res.ok) {
        const profile = await res.json();
        setUser(prev => prev ? {
          ...prev,
          name: profile.name,
          email: profile.email,
          role: profile.role,
        } : prev);
      }
    } catch {
      // Profile fetch is best-effort
    }
  };

  const setCookieSecure = (token: string) => {
    const isSecure = typeof window !== 'undefined' && window.location.protocol === 'https:';
    document.cookie = `jwt_token=${token}; path=/; max-age=86400; SameSite=Lax${isSecure ? '; Secure' : ''}`;
  };

  // Check for existing token on mount
  useEffect(() => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      const tokenPayload = parseJwt(token);
      if (tokenPayload && tokenPayload.exp * 1000 > Date.now()) {
        setUser({
          jwt_token: token,
          user_id: tokenPayload.user_id || '',
          expires_at: new Date(tokenPayload.exp * 1000).toISOString(),
          is_authenticated: true,
        });
        fetchProfile(token);
      }
    }
    setIsLoading(false);
  }, []);

  const signIn = async (email: string, password: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Sign in failed' }));
      throw new Error(errorData.detail || `Sign in failed: ${response.status}`);
    }

    const data = await response.json();
    const token = data.data?.token;

    if (!token) {
      throw new Error('Token not found in response');
    }

    localStorage.setItem('jwt_token', token);
    setCookieSecure(token);

    const tokenPayload = parseJwt(token);
    setUser({
      jwt_token: token,
      user_id: tokenPayload.user_id || data.data?.user_id || '',
      expires_at: data.data?.expires_at || new Date(tokenPayload.exp * 1000).toISOString(),
      is_authenticated: true,
    });

    fetchProfile(token);
    router.push('/dashboard');
  };

  const signUp = async (email: string, password: string, name: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Sign up failed' }));
      throw new Error(errorData.detail || `Sign up failed: ${response.status}`);
    }

    const data = await response.json();
    const token = data.data?.token;

    if (!token) {
      throw new Error('Token not found in response');
    }

    localStorage.setItem('jwt_token', token);
    setCookieSecure(token);

    const tokenPayload = parseJwt(token);
    setUser({
      jwt_token: token,
      user_id: tokenPayload.user_id || data.data?.user_id || '',
      expires_at: data.data?.expires_at || new Date(tokenPayload.exp * 1000).toISOString(),
      is_authenticated: true,
    });

    fetchProfile(token);
    router.push('/dashboard');
  };

  const signOut = async () => {
    localStorage.removeItem('jwt_token');
    document.cookie = 'jwt_token=; path=/; max-age=0';
    setUser(null);
    router.push('/');
  };

  const getToken = () => {
    return localStorage.getItem('jwt_token');
  };

  const value = {
    user,
    isLoading,
    signIn,
    signUp,
    signOut,
    getToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
