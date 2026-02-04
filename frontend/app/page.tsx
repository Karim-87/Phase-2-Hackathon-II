'use client';

import Link from 'next/link';
import { useAuth } from '@/components/auth/auth-provider';
import ModernButton from '@/components/ui/modern-button';
import DashboardPage from './dashboard/page';

export default function HomePage() {
  const { user, isLoading } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] p-4">
      <h1 className="text-4xl font-bold text-[rgb(var(--text-primary))] mb-6">Welcome to Todo App</h1>
      <p className="text-lg text-[rgb(var(--text-secondary))] mb-8 text-center max-w-md">
        A multi-user todo application with Eisenhower Matrix prioritization
      </p>

      {isLoading ? (
        <p>Loading...</p>
      ) : user ? (
        <Link href="/dashboard">
          <ModernButton variant="primary">
            Go to Dashboard
          </ModernButton>
        </Link>
      ) : (
        <div className="space-y-4">
          <Link href="/sign-in">
            <ModernButton variant="primary" className="w-full">
              Sign In
            </ModernButton>
          </Link>
          <Link href="/sign-up">
            <ModernButton variant="secondary" className="w-full">
              Sign Up
            </ModernButton>
          </Link>
        </div>
        
      )} 
    </div>
  );
}