'use client';

import Link from 'next/link';
import { useAuth } from '@/components/auth/auth-provider';
import ModernButton from '@/components/ui/modern-button';
import { LoadingSpinner } from '@/components/ui/loading-spinner';

export default function HomePage() {
  const { user, isLoading } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 py-8">
      <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-[rgb(var(--text-primary))] mb-6 text-center">
        Welcome to Todo App
      </h1>
      <p className="text-base sm:text-lg text-[rgb(var(--text-secondary))] mb-8 text-center max-w-md">
        A multi-user todo application with Eisenhower Matrix prioritization
      </p>

      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : user ? (
        <Link href="/dashboard">
          <ModernButton variant="primary">
            Go to Dashboard
          </ModernButton>
        </Link>
      ) : (
        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 w-full max-w-xs">
          <Link href="/sign-in" className="flex-1">
            <ModernButton variant="primary" className="w-full">
              Sign In
            </ModernButton>
          </Link>
          <Link href="/sign-up" className="flex-1">
            <ModernButton variant="secondary" className="w-full">
              Sign Up
            </ModernButton>
          </Link>
        </div>
      )}
    </div>
  );
}
