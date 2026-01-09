'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { User, UserRegister, UserLogin, AuthToken } from '@/types/user';
import { api, handleError } from '@/lib/api';
import { setUserSession, getUserSession, clearAuthToken } from '@/lib/auth';

interface UseAuthReturn {
  user: User | null;
  loading: boolean;
  error: string | null;
  register: (data: UserRegister) => Promise<void>;
  login: (data: UserLogin) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  clearError: () => void;
}

/**
 * Authentication hook for managing user state and auth operations
 * Provides register, login, logout, and session management
 */
export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  /**
   * Fetch current user from session or API
   */
  const refreshUser = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Check local session first
      const session = getUserSession();
      if (session) {
        setUser(session.user);
        setLoading(false);
        return;
      }

      // Fetch from API if no local session
      const currentUser = await api.get<User>('/api/auth/me');
      setUser(currentUser);

      // Update session
      setUserSession({
        user: currentUser,
        accessToken: '', // Token already in cookies
        expiresAt: Date.now() + 24 * 60 * 60 * 1000, // 24 hours
      });
    } catch (err) {
      // User not authenticated, clear state
      setUser(null);
      clearAuthToken();
      setError(null); // Don't show error on initial load
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Register new user
   */
  const register = useCallback(
    async (data: UserRegister) => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.post<AuthToken>('/api/auth/register', data, false);

        // Store session
        setUserSession({
          user: response.user,
          accessToken: response.access_token,
          expiresAt: Date.now() + 24 * 60 * 60 * 1000,
        });

        setUser(response.user);

        // Redirect to dashboard
        router.push('/dashboard');
      } catch (err) {
        const errorMessage = handleError(err);
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [router]
  );

  /**
   * Login existing user
   */
  const login = useCallback(
    async (data: UserLogin) => {
      setLoading(true);
      setError(null);

      try {
        // FastAPI expects form data for OAuth2PasswordRequestForm
        const formData = new URLSearchParams();
        formData.append('username', data.email);
        formData.append('password', data.password);

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/login`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Invalid credentials');
        }

        const authData = await response.json() as AuthToken;

        // Store session
        setUserSession({
          user: authData.user,
          accessToken: authData.access_token,
          expiresAt: Date.now() + 24 * 60 * 60 * 1000,
        });

        setUser(authData.user);

        // Redirect to dashboard
        router.push('/dashboard');
      } catch (err) {
        const errorMessage = handleError(err);
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [router]
  );

  /**
   * Logout user
   */
  const logout = useCallback(() => {
    clearAuthToken();
    setUser(null);
    router.push('/login');
  }, [router]);

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  /**
   * Load user on mount
   */
  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  return {
    user,
    loading,
    error,
    register,
    login,
    logout,
    refreshUser,
    clearError,
  };
}
