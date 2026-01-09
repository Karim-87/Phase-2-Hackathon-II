import { useState, useEffect } from 'react';
import { authClient } from '@/lib/auth/auth-client';
import { UserSession } from '@/types/user';

export function useAuth() {
  const [user, setUser] = useState<UserSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing user session on mount
    const userSession = authClient.getUserFromToken();
    setUser(userSession);
    setIsLoading(false);

    // Set up a timer to check for token expiration
    const checkTokenExpiration = () => {
      const token = authClient.getToken();
      if (token && authClient.isTokenExpired(token)) {
        // Token is expired, remove it and update state
        authClient.removeToken();
        setUser(null);
      }
    };

    // Check token expiration every minute
    const interval = setInterval(checkTokenExpiration, 60000);

    return () => clearInterval(interval);
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      // In a real app, this would make an API call to your backend
      // For now, we'll simulate the response
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Sign in failed');
      }

      const data = await response.json();
      const token = data.token;

      authClient.setToken(token);
      const userSession = authClient.getUserFromToken();
      setUser(userSession);

      return data;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async (email: string, password: string, name: string) => {
    try {
      // In a real app, this would make an API call to your backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        throw new Error('Sign up failed');
      }

      const data = await response.json();
      const token = data.token;

      authClient.setToken(token);
      const userSession = authClient.getUserFromToken();
      setUser(userSession);

      return data;
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = () => {
    authClient.removeToken();
    setUser(null);
  };

  const getToken = () => {
    return authClient.getToken();
  };

  return {
    user,
    isLoading,
    signIn,
    signUp,
    signOut,
    getToken,
  };
}