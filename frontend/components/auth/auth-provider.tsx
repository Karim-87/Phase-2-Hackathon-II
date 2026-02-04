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

  // Check for existing token on mount
  useEffect(() => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      // Verify token is still valid
      const tokenPayload = parseJwt(token);
      if (tokenPayload && tokenPayload.exp * 1000 > Date.now()) {
        // Token is valid, but we don't have user details yet
        // We'll need to call an API to get user details
        // For now, we'll just set a minimal user object
        setUser({
          jwt_token: token,
          user_id: tokenPayload.user_id || '',  // Backend sends 'user_id', not 'userId'
          expires_at: new Date(tokenPayload.exp * 1000).toISOString(),
          is_authenticated: true,
        });
      }
    }
    setIsLoading(false);
  }, []);

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
    } catch (e) {
      console.error('Failed to parse JWT:', e);
      return null;
    }
  };

  const signIn = async (email: string, password: string) => {
    try {
      console.log('SignIn: Starting...', { email, apiUrl: process.env.NEXT_PUBLIC_API_BASE_URL });

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      console.log('SignIn: Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Sign in failed' }));
        console.error('SignIn: Error response:', errorData);
        throw new Error(errorData.detail || `Sign in failed: ${response.status}`);
      }

      const data = await response.json();
      console.log('SignIn: Success data:', data);
      const token = data.data?.token;

      if (!token) {
        throw new Error('Token not found in response');
      }

      localStorage.setItem('jwt_token', token);
      // Also set cookie for middleware access
      document.cookie = `jwt_token=${token}; path=/; max-age=${60 * 60 * 24}`; // 24 hours
      console.log('SignIn: Token saved to localStorage and cookie');

      // Parse token to get user info
      const tokenPayload = parseJwt(token);
      console.log('SignIn: Token payload:', tokenPayload);

      setUser({
        jwt_token: token,
        user_id: tokenPayload.user_id || data.data?.user_id || '',  // Backend sends 'user_id', not 'userId'
        expires_at: data.data?.expires_at || new Date(tokenPayload.exp * 1000).toISOString(),
        is_authenticated: true,
      });

      console.log('SignIn: Redirecting to dashboard...');
      router.push('/dashboard');
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async (email: string, password: string, name: string) => {
    try {
      console.log('Attempting signup with:', { email, name, apiUrl: process.env.NEXT_PUBLIC_API_BASE_URL });

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      console.log('Signup response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Sign up failed' }));
        console.error('Signup error response:', errorData);
        throw new Error(errorData.detail || `Sign up failed: ${response.status}`);
      }

      const data = await response.json();
      console.log('Signup success, received data');

      const token = data.data?.token;

      if (!token) {
        throw new Error('Token not found in response');
      }

      localStorage.setItem('jwt_token', token);
      // Also set cookie for middleware access
      document.cookie = `jwt_token=${token}; path=/; max-age=${60 * 60 * 24}`; // 24 hours

      // Parse token to get user info
      const tokenPayload = parseJwt(token);
      setUser({
        jwt_token: token,
        user_id: tokenPayload.user_id || data.data?.user_id || '',  // Backend sends 'user_id', not 'userId'
        expires_at: data.data?.expires_at || new Date(tokenPayload.exp * 1000).toISOString(),
        is_authenticated: true,
      });

      router.push('/dashboard');
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = async () => {
    localStorage.removeItem('jwt_token');
    // Also remove cookie
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